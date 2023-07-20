from rest_framework import viewsets


from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        match self.request.method:
            case "GET":
                return self.get_queryset()

        return self.get_queryset().filter(pk=self.request.user.id)
