from rest_framework import serializers
from .models import Channel, Topic, Reply
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Topic
        fields = '__all__'

class TopicListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'channel', 'status',  'owner', 'top', 'created', ]


class ReplyListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Reply
        fields = '__all__'
