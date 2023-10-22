from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.decorators import action, permission_classes, authentication_classes


from .models import Notification, Profile, User
from .serializers import NotificationSerializer, UserSerializer, ProfileSerializer
from .authentication import FirebaseTokenAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related(
        "profile",
        "settings",
        "purchases",
    )
    serializer_class = UserSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser, FileUploadParser]

    @permission_classes([AllowAny])
    @authentication_classes([FirebaseTokenAuthentication])
    def create(self, request: Request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(
        detail=False,
        url_path="current-user",
        authentication_classes=[FirebaseTokenAuthentication],
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

        return (
            super()
            .get_queryset()
            .filter(
                pk=self.request.user.id,
            )
        )


class ProfileSerializer(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
