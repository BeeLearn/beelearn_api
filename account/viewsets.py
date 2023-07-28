from rest_framework import viewsets, exceptions, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes


from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path="current-user")
    def current_user(self, request: Request):
        return Response(
            self.get_serializer(instance=request.user).data,
        )

    @action(["post"], detail=False, url_path="create-user")
    @permission_classes([permissions.AllowAny])
    def create_user(self, request: Request):
        device_id = request.data.get("device_id")

        if not device_id:
            raise exceptions.ParseError("device_id is required")

        user, created = User.objects.get_or_create(username=device_id)

        token, created = Token.objects.get_or_create(user=user)

        return Response({"key": token.key })

    def get_queryset(self):
        match self.request.method:
            case "GET":
                return super().get_queryset()

        return super().get_queryset().filter(pk=self.request.user.id)
