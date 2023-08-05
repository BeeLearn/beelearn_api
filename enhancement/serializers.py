from rest_framework import serializers

from catalogue.serializers import TopicSerializer

from .models import Enhancement


class EnhancementSerializer(serializers.ModelSerializer):
    """
    Enhancement model serializer
    """
    topic = TopicSerializer()
    
    class Meta:
        model = Enhancement
        exclude = ("user",)