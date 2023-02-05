from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(label='Повторите пароль')

    def create(self, validated_data):
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError("Password mismatch")

        user = User.objects.create_user(validated_data['username'], email=getattr(validated_data, 'email', ''),
                                        password=validated_data['password'],
                                        first_name=getattr(validated_data, 'first_name', ''),
                                        last_name=getattr(validated_data, 'last_name', ''))
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
