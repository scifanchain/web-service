from rest_framework import serializers
from .models import Topic, Reply
from django.contrib.auth.models import User


class TopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
