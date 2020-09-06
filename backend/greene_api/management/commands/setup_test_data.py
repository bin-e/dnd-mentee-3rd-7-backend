import random

import factory
from django.db import transaction
from django.core.management.base import BaseCommand

from ...models import User, Post, Hashtag, History, Like
from ...factories import (
    UserFactory,
    PostFactory,
    CommentFactory,
    HashtagFactory,
    HistoryFactory,
    LikeFactory,
)

NUM_USERS = 100
NUM_POSTS = 200
NUM_COMMENTS = 300
NUM_HASHTAGES = 30
USERS_PER_HASHTAG = 3
NUM_HISTORYS = 500
NUM_LIKES = 30

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Post, Hashtag, History]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create a superuser
        superuser = UserFactory(
            email='greene@gmail.com',
            username = 'greene',
            password=factory.PostGenerationMethodCall('set_password', 'greene'),
            is_staff=True,
            is_superuser=True,
            )
        
        # Create all the users
        people = []
        for _ in range(NUM_USERS):
            person = UserFactory()
            people.append(person)
            
        # Create hashtags
        hashtags = []
        for _ in range(NUM_HASHTAGES):
            hashtag = HashtagFactory()
            hashtags.append(hashtag)
        
        posts = []
        # Create posts that is associated with user
        for _ in range(NUM_POSTS):
            user = random.choice(people)
            post = PostFactory(user=user)
            posts.append(post)
            htgs = random.choices(hashtags, k=USERS_PER_HASHTAG)
            post.hashtags.add(*htgs)
        
        # Create comments that is associated with user and post
        for _ in range(NUM_COMMENTS):
            user = random.choice(people)
            post = random.choice(posts)
            comment = CommentFactory(user=user, post=post)
            
        # Create historys
        for _ in range(NUM_HISTORYS):
            user = random.choice(people)
            history = HistoryFactory(user=user)
            
        # Create Likes 
        for _ in range(NUM_LIKES):
            user = random.choice(people)
            post = random.choice(posts)
            like = LikeFactory(user=user, post=post, number=random.randint(1, 5))

