from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.mixins import DynamicFieldsMixin
from django_restql.serializers import NestedModelSerializer

from account.serializers import UserSerializer

from beelearn.mixins import ContextMixin

from .models import Comment, Reply, Thread


class CommentSerializer(NestedModelSerializer, ContextMixin, DynamicFieldsMixin):
    """
    Comment model serializer
    """

    user = UserSerializer(exclude=["profile", "settings"])

    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    likes = NestedField(
        UserSerializer,
        write_only=True,
    )

    def get_is_liked(self, comment: Comment):
        return comment.likes.contains(self.request.user)

    def get_like_count(self, comment: Comment):
        return comment.likes.count()

    class Meta:
        model = Thread
        exclude = ("replies",)
        extra_kwargs = {
            "likes": {
                "write_only": True,
            }
        }


class ThreadSerializer(CommentSerializer):
    """
    Thread model serializer
    """

    replies = CommentSerializer(many=True)

    class Meta:
        model = Thread
        fields = "__all__"


class ReplySerializer(serializers.ModelSerializer):
    """
    Reply model serializer
    """

    parent = NestedModelSerializer(
        ThreadSerializer,
        write_only=True,
    )
    comment = NestedModelSerializer(
        ThreadSerializer,
        write_only=True,
    )

    class Meta:
        model = Reply
        fields = "__all__"
