from rest_framework import viewsets

from account.models import UserCourse

from .serializers import UserCourseSerializer


class UserCourseViewSet(viewsets.ModelViewSet):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer
    filter_fields = ["is_complete"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
