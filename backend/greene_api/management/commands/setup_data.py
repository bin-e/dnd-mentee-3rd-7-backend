import random

from django.db import transaction
from django.core.management.base import BaseCommand

from .models import User, Post, Hashtag, History
from .factories import (
    UserFactory,
    PostFactory,
    HashtagFactory,
    HistoryFactory
)

NUM_USERS = 30
NUM_POSTS = 100
NUM_HASHTAGES = 12
COMMENTS_PER_THREAD = 25
USERS_PER_HASHTAG = 4

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Post, Hashtag, History]
        for model in models:
            model.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        people = []
        for _ in range(NUM_USERS):
            person = UserFactory()
            people.append(person)

        # Add some users to posts
        for _ in range(NUM_POSTS):
            user = random.choice(people)
            post = PostFactory(user=user)
      
        # Create hashtags
        for _ in range(NUM_HASHTAGES):
            members = random.choices(people, k=USERS_PER_HASHTAG)
            hashtag = HashtagFactory()
            hashtag.user.add(*members)
