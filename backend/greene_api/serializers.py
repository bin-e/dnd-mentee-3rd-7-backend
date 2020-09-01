from rest_framework import serializers
from .models import User, Post, Hashtag, History


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
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 
        'last_login', 'date_joined',)
        read_only_fields = ('first_name', 'last_name', 'last_login', 'date_joined',)
        extra_kwargs = {'password': {'write_only': True}}


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # refer https://stackoverflow.com/questions/61537923/update-manytomany-relationship-in-django-rest-framework
    # have to write a update and create_or_update for put method
    username = serializers.SerializerMethodField()
    hashtags = HashtagSerializer(many=True)

    def get_username(self, obj):
        return obj.user.username

    def get_or_create_hashtags(self, hashtags):
        hashtag_ids = []
        for hashtag in hashtags:
            # find hashtags using a hashtag name
            hashtag_instance, created = Hashtag.objects.get_or_create(name=hashtag.get('name'), defaults=hashtag)
            hashtag_ids.append(hashtag_instance.pk)
        return hashtag_ids

    def create(self, validated_data):
        hashtags_validated_data = validated_data.pop('hashtags')
        post = Post.objects.create(**validated_data)
        post.hashtags.set(self.get_or_create_hashtags(hashtags_validated_data))
        return post

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'like', 'thumbnail', 'thumbnail',
         'user', 'username', 'hashtags',)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
