from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', ]

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, username):
        """
        Check whether length of username more than six characters long.
        """
        if len(username) < 6:
            raise serializers.ValidationError("length of username more than six characters long")
        return username

    def validate_password(self, password):
        """
        Check whether length of password more than six characters long.
        """
        if len(password) < 6:
            raise serializers.ValidationError("length of password more than six characters long")
        return password