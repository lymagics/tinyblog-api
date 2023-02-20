from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomeUserCreationForm(UserCreationForm):
    """
    Custom user creation form used in admin panel.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form used in admin panel.
    """

    class Meta:
        model = User
        fields = ('username', 'email',)
