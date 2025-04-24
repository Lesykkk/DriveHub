from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class AccountLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class AccountRegistrationForm(CustomUserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'password1',
            'password2',
        )


class ProfileForm(CustomUserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone',
            'password',
        )