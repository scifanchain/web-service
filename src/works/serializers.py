from rest_framework import serializers
from .models import Stage


class StageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = [
            'id',
            'title',
            'content',
            'owner',
            'created',
            'updated',
        ]


class StageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'
