from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import CustomUser


class AccountLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    error_messages = {
        "invalid_login": _(
            "Please enter correct credentials."
        ),
        "inactive": _("This account is inactive."),
    }


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
            'new_password',
        )
    
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            try:
                validate_password(new_password, user=self.instance)
            except ValidationError as errors:
                raise ValidationError(errors)
        return new_password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user

