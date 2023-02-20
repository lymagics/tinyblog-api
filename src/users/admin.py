from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .forms import CustomeUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Django admin model to represent User model in admin panel.
    """

    model = User
    add_form = CustomeUserCreationForm
    form = CustomUserChangeForm
    list_display = ('id', 'username', 'email',)
    list_display_links = ('id', 'username',)
