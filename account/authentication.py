from django.contrib.auth.models import AbstractUser

from rest_framework.authentication import TokenAuthentication

from firebase_admin.auth import verify_id_token

from djira.authentication import TokenAuthentication as DjiraTokenAuthentication

from .models import User


def authenticate_credentials(key: str):
    decoded_token = verify_id_token(key)
    user, created = User.objects.get_or_create(
        uid=decoded_token["uid"],
        username=decoded_token["uid"]
    )

    if created:
        user.email = decoded_token["email"]
        user.save(update_fields=["email"])

    return user, key


class FirebaseTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        return authenticate_credentials(key)


class DjiraFirebaseTokenAuthentication(DjiraTokenAuthentication):
    def authenticate_credential(self, key: str) -> AbstractUser:
        return authenticate_credentials(key)[0]
