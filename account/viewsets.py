from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, permission_classes, authentication_classes


from .models import Notification, Settings, User
from .serializers import NotificationSerializer, SettingsSerializer, UserSerializer
from .authentication import FirebaseTokenAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @permission_classes([AllowAny])
    @authentication_classes([FirebaseTokenAuthentication])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(
        detail=False,
        url_path="current-user",
    )
    def current_user(self, request: Request):
        return Response(
            self.get_serializer(instance=request.user).data,
        )

    @current_user.mapping.patch
    def update_current_user(self, request: Request):
        serializer: UserSerializer = self.get_serializer(
            instance=request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get_queryset(self):
        match self.request.method:
            case "GET":
                return super().get_queryset()

        return super().get_queryset().filter(pk=self.request.user.id)


class SettingsViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Settings.objects.all()

    serializer_class = SettingsSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
