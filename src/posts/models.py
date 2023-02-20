from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    Django ORM model to represent 'posts' table.
    """

    text = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.text[:20]
