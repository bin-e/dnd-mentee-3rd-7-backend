import random 

import factory
from factory.django import DjangoModelFactory

from .models import User, Post, Comment, Hashtag, History, Like


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    name = factory.Faker('name')
    username = factory.Sequence(lambda n: 'user%s' % n)
    email = factory.Faker('email')
    is_superuser = False
    is_staff = False
    is_active = True


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = factory.Faker(
        'sentence',
        nb_words=5,
        variable_nb_words=True
    )
    content = factory.Faker(
        'sentence',
        nb_words=20,
        variable_nb_words=True
    )
    

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
        
    content = factory.Faker(
        'sentence',
        nb_words=10,
        variable_nb_words=True
    )


class HashtagFactory(DjangoModelFactory):
    class Meta:
        model = Hashtag
        
    name = factory.Faker('word')


class HistoryFactory(DjangoModelFactory):
    class Meta:
        model = History
        
    query = factory.Faker('word')
    


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like
    