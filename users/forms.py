from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
