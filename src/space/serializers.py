from rest_framework import serializers
from django.contrib.auth.models import User
from space.models import Wallet

class UserRegisterSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail', lookup_field='username')

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserDescSerializer(serializers.ModelSerializer):
    """可用于其它视图中引用的嵌套序列化器"""

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_login',
            'date_joined'
        ]


class WalletSerializer(serializers.ModelSerializer):
    """钱包序列化器"""

    owner = UserDescSerializer(read_only=True)  # 嵌套作者序列化信息
    
    class Meta:
        model = Wallet
        fields = '__all__'
