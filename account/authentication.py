from django.contrib.auth.models import AbstractUser

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, NotAcceptable

from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError
from firebase_admin.auth import verify_id_token, get_user, UserRecord

from djira.authentication import TokenAuthentication as DjiraTokenAuthentication

from .models import Profile, User


def authenticate_credentials(key: str):
    decoded_token = verify_id_token(key)
    user, created = User.objects.get_or_create(
        uid=decoded_token["uid"],
    )

    firebase_user: UserRecord = get_user(decoded_token["uid"])
    user.email = decoded_token["email"]

    if created:
        user.username = decoded_token["uid"]
        names: str = firebase_user.display_name
        if names:
            names = names.strip().split(" ")

            if len(names) > 0:
                user.last_name = names[1]

            user.first_name = names[0]
    try:
        user.profile.email_verified = firebase_user.email_verified
        user.profile.save(update_fields=["is_email_verified"])
    except Profile.DoesNotExist:
        # race condition issues, not likeable to occur
        raise NotFound(
            {
                "message": "user does not have a profile.",
            },
            "profile/no-found",
        )

    user.save(update_fields=["email", "first_name", "last_name", "username"])

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
