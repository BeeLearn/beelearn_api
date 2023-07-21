from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action


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

    def get_queryset(self):
        match self.request.method:
            case "GET":
                return super().get_queryset()

        return super().get_queryset().filter(pk=self.request.user.id)
