from hashlib import md5

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Django ORM model to represent 'users' table.
    """

    email = models.EmailField(unique=True)
    about_me = models.TextField(default='')
    last_seen = models.DateTimeField(default=timezone.now)
    first_seen = models.DateTimeField(auto_now_add=True)

    @property
    def avatar_url(self):
        avatar_hash = md5(self.email.encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{avatar_hash}?d=mp'

    def __str__(self):
        return self.username
