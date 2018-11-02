from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'firstname', 'lastname',
                  'password')

        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """docstring for LoginSerializer"""
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=16, min_length=7, required=True)

    class Meta:
        """docstring for Meta"""
        fields = ('email', 'password')
