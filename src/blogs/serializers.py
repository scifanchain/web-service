from rest_framework import serializers
from .models import Category, Post, Archive, Comment


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'summary',
            'owner',
            'created',
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
