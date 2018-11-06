from rest_framework import serializers

from .models import PersonalInfo, User


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
    password = serializers.CharField(
        max_length=16, min_length=7, required=True)

    class Meta:
        """docstring for Meta"""
        fields = ('email', 'password')


class PersonalInfoSerializer(serializers.ModelSerializer):
    """docstring for PersonalInfoSerializer"""
    class Meta:
        model = PersonalInfo
        exclude = ('user',)
        extra_kwargs = {'country': {'required': True},
                        'state': {'required': True},
                        'city': {'required': True}}

    def create(self, validated_data):
        user = self.context.get('user')
        personal_info = PersonalInfo.objects.create(
            **validated_data, **{"user_id": user.id})
        return personal_info

    def update(self, instance, validated_data):
        print("I AM INSIDE UPDATE METHOD")
        instance.address1 = validated_data.get("address1", instance.address1)
        instance.address2 = validated_data.get("address2", instance.address2)
        instance.secondary_email = validated_data.get(
            "secondary_email", instance.secondary_email)
        instance.mobile_number = validated_data.get(
            "mobile_number", instance.mobile_number)
        instance.state = validated_data.get("state", instance.state)
        instance.city = validated_data.get("city", instance.city)
        instance.country = validated_data.get("country", instance.country)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.save()
        return instance
