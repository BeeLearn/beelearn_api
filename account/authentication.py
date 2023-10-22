from django.contrib.auth.models import AbstractUser

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, NotAcceptable

from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError
from firebase_admin.auth import verify_id_token, get_user, UserRecord

from djira.authentication import TokenAuthentication as DjiraTokenAuthentication

from .models import Profile, User


def get_first_and_last_name(full_name: str):
    first_name, last_name = None, None

    if full_name:
        names = full_name.strip().split(" ")
        first_name = names[0]

        if len(names) > 0:
            last_name = names[1]

    return first_name, last_name


def authenticate_credentials(key: str):
    decoded_token = verify_id_token(key)
    firebase_user: UserRecord = get_user(decoded_token["uid"])

    first_name, last_name = get_first_and_last_name(firebase_user.display_name)

    user, created = User.objects.get_or_create(
        uid=decoded_token["uid"],
        defaults={
            "last_name": last_name,
            "first_name": first_name,
            "username": decoded_token["uid"],
            "email": decoded_token["email"],
        },
    )

    try:
        if user.profile.is_email_verified != firebase_user.email_verified:
            user.profile.is_email_verified = firebase_user.email_verified
            user.profile.save(update_fields=["is_email_verified"])
    except Profile.DoesNotExist:
        # race condition issues, not likeable to occur
        raise NotFound(
            {
                "message": "user does not have a profile.",
            },
            "profile/no-found",
        )

    user.save(
        update_fields=[
            "email",
            "first_name",
            "last_name",
            "username",
        ],
    )

    return user, key


class FirebaseTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            return authenticate_credentials(key)
        except ExpiredIdTokenError as error:
            raise NotAcceptable(
                {
                    "message": "expired firebase idToken",
                },
                "auth/expired-token",
            ) from error
        except InvalidIdTokenError as error:
            raise NotAcceptable(
                {
                    "message": "invalid firebase idToken",
                },
                "auth/invalid-token",
            ) from error


class DjiraFirebaseTokenAuthentication(DjiraTokenAuthentication):
    def authenticate_credential(self, key: str) -> AbstractUser:
        return authenticate_credentials(key)[0]
