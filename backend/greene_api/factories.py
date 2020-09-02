import random 

from factory.django import DjangoModelFactory
from .models import User, Post, Hashtag, History


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    name = factory.Faker('name')
    # username = factory.Sequence(lambda n: 'user%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
    is_superuser = False
    is_staff = False


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )
    content = factory.Faker("sentence")
    like = random.choices([0, 1, 2, 3, 4, 5])


class HashtagFactory(DjangoModelFactory):
    class Meta:
        model = Hashtag


class HistoryFactory(DjangoModelFactory):
    class Meta:
        model = History
    
