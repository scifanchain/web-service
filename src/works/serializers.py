from rest_framework import serializers
from .models import Stage
from authors.serializers import UserDescSerializer


# Stage 视图集序列化器
# 自动提供了外键字段的超链接
# 默认不包含模型对象的 id 字段
class StageSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserDescSerializer(read_only=True) # 嵌套作者序列化信息
    class Meta:
        model = Stage
        fields = '__all__'

# Stage 列表序列化器
class StageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = [
            'id',
            'title',
            'owner',
            'created',
            'updated',
        ]
        read_only_fields = ['owner']


# Stage 详情序列化器
class StageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'


