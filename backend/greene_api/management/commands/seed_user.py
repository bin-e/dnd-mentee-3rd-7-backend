import random

from django_seed import Seed
from django.core.management.base import BaseCommand
from ...models import User, Post

class Command(BaseCommand):
    help = "This command creates users & posts"

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=1, type=int, help="How many users do you want to create?"
        )
    
    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {
            'is_staff': False,
            'is_superuser': False,
        })
        inserted_pks = seeder.execute()

        seeder = Seed.seeder()
        for pk in list(inserted_pks.values())[0]:
            seeder.add_entity(Post, random.randint(0, 5), {
                'user': User.objects.get(id=pk),
            })
        
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f'{number} users and posts created!'))