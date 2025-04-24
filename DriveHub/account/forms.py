from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

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
        fields = ['email', 'password']


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
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone',
            'password',
        )