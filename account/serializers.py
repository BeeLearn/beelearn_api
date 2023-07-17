from rest_framework import serializers

from account.models import UserCourse
from catalogue.serializers import CourseSerializer, LessonSerializer


class UserCourseSerializer(serializers.ModelSerializer):
    """
    UserCourse model serializer
    """

    user_id = serializers.IntegerField(write_only=True)
    course = CourseSerializer()
    last_lesson = LessonSerializer()

    class Meta:
        model = UserCourse
        exclude = ("user",)
