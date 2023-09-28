from rest_framework import serializers

from django_restql.fields import NestedField
from django_restql.mixins import DynamicFieldsMixin
from django_restql.serializers import NestedModelSerializer

from account.serializers import UserSerializer

from beelearn.mixins import ContextMixin

from .models import Comment, Reply, Thread


class SubCommentSerializer(NestedModelSerializer, ContextMixin, DynamicFieldsMixin):
    """
    Comment model serializer
    """

    user = UserSerializer(
        exclude=["profile", "settings", "token"],
        default=serializers.CurrentUserDefault(),
    )

    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    likes = NestedField(
        UserSerializer,
        many=True,
        write_only=True,
        required=False,
    )

    def get_is_liked(self, comment: Comment):
        return comment.likes.contains(self.request.user)

    def get_like_count(self, comment: Comment):
        return comment.likes.count()

    class Meta:
        model = Comment
        exclude = ("replies",)


class CommentSerializer(SubCommentSerializer):
    """
    Comment model serializer
    """

    replies = SubCommentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = "__all__"


class ThreadSerializer(NestedModelSerializer):
    """
    Thread model serializer
    """

    comment = NestedField(
        CommentSerializer,
    )

    class Meta:
        model = Thread
        fields = "__all__"


class ReplySerializer(NestedModelSerializer):
    """
    Reply model serializer
    """

    comment = NestedField(SubCommentSerializer)

    class Meta:
        model = Reply
        fields = "__all__"
