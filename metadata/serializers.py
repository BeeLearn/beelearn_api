from rest_framework import serializers

from .models import Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ()
