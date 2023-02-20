from django.core.management.base import BaseCommand

from faker import Faker

from users.models import User

faker = Faker()


class Command(BaseCommand):
    help = 'Create the given number of fake users.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of fake users')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for _ in range(total):
            User.objects.create_user(
                username=faker.user_name(), email=faker.email(),
                about_me=faker.sentence(), password='testpass123',
            )
        self.stdout.write(f'{total} users added.')
