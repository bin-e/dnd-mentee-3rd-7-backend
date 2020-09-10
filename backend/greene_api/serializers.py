from django.db.models import Sum

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Post, Comment, Hashtag, History, Like, File


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
        fields = ('id', 'email', 'name', 'username', 'password', 'last_login', 'date_joined',)
        read_only_fields = ('last_login', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }
        

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # refer https://stackoverflow.com/questions/61537923/update-manytomany-relationship-in-django-rest-framework
    # have to write a update and create_or_update for put method
    username = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
    hashtags = HashtagSerializer(many=True)
    
    def get_username(self, obj):
        return obj.user.username

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    def get_number_of_likes(self, obj):
        number_of_likes = Like.objects.filter(post=obj).aggregate(Sum('number'))
        return number_of_likes.get('number__sum') \
            if number_of_likes.get('number__sum') is not None \
                else 0
    
    def get_or_create_hashtags(self, hashtags):
        hashtag_ids = []
        for hashtag in hashtags:
            # find hashtags using a hashtag name
            hashtag_instance, created = Hashtag.objects.get_or_create( \
                name=hashtag.get('name'), defaults=hashtag)
            hashtag_ids.append(hashtag_instance.pk)
        return hashtag_ids

    def create(self, validated_data):
        hashtags_validated_data = validated_data.pop('hashtags')
        post = Post.objects.create(**validated_data)
        post.hashtags.set(self.get_or_create_hashtags(hashtags_validated_data))
        return post

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'thumbnail', \
            'user', 'username', 'hashtags', 'number_of_comments', \
                'number_of_likes', 'date_created', 'date_modified',)
        read_only_fields = ('date_created', 'date_modified',)


class CommentSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('date_created', 'date_modified',)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        like_instance, created = Like.objects.get_or_create(user=validated_data.get('user'), \
            post=validated_data.get('post'), defaults=validated_data)
        like_instance.number += 1
        like_instance.save()
        return like_instance
    
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'number', 'date_created', 'date_modified',)
        read_only_fields = ('number', 'date_created', 'date_modified',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenBlacklistSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        self.refresh_token = attrs['refresh']
        RefreshToken(attrs['refresh'])
        return data

    def save(self, **kwargs):
        RefreshToken(self.refresh_token).blacklist()


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'