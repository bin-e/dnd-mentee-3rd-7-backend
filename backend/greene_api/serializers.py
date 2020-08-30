from rest_framework import serializers
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
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

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'last_login', 'date_joined',)
        read_only_fields = ('first_name', 'last_name', 'last_login', 'date_joined',)
        extra_kwargs = {'password': {'write_only': True}}


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = ('title', 'content', 'like', 'thumbnail', 'thumbnail', 'user', 'username',)
