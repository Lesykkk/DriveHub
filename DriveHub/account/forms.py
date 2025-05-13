from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import CustomUser


class AccountLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class AccountRegistrationForm(UserCreationForm):
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



class ProfileForm(UserChangeForm):
    password = None
    new_password = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone',
            'new_password'
        )