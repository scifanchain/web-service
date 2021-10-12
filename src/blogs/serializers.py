from rest_framework import serializers
from .models import Category, Post, Archive, Comment
from django.contrib.auth.models import User


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BlogListSerializer(serializers.ModelSerializer):
    # category = CategoryListSerializer()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'summary',
            'owner',
            'created',
            'category'
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    owner = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'
