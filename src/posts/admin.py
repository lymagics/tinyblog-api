from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Django admin model to represent Post model in admin panel.
    """

    list_display = ('id', 'text',)
