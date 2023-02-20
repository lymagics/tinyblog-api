from random import choice

from django.core.management.base import BaseCommand

from faker import Faker

from users.models import User
from posts.models import Post

faker = Faker()


class Command(BaseCommand):
    help = 'Create the given number of fake posts, assigned to random users.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of fake posts.')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        users = User.objects.all()

        for _ in range(total):
            author = choice(users)
            Post.objects.create(
                text=faker.paragraph(), author=author,
                timestamp=faker.date_time_this_year(),
            )

        self.stdout.write(f'{total} posts added.')
