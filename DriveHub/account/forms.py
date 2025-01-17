from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Account


class AccountLoginForm(AuthenticationForm):
    class Meta:
        model = Account
        fields = ['username', 'password']


class AccountRegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'password1',
            'password2',
        )


class ProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
        )