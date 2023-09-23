from django.contrib.auth.models import AbstractUser

from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication

from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError
from firebase_admin.auth import verify_id_token, get_user, UserRecord

from djira.authentication import TokenAuthentication as DjiraTokenAuthentication

from .models import User


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

    user.profile.email_verified = firebase_user.email_verified
    user.profile.save(update_fields=["is_email_verified"])

    user.save(update_fields=["email", "first_name", "last_name", "username"])

    return user, key


class FirebaseTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            return authenticate_credentials(key)
        except ExpiredIdTokenError:
            raise APIException("Expired token")
        except InvalidIdTokenError as error:
            print(error)
            raise APIException("Invalid token")


class DjiraFirebaseTokenAuthentication(DjiraTokenAuthentication):
    def authenticate_credential(self, key: str) -> AbstractUser:
        return authenticate_credentials(key)[0]
