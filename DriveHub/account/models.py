from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    phone_validator = RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )

    username = None
    phone = models.CharField(
        _("phone number"),
        max_length=20,
        unique = True,
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        unique = True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()
    
    def __str__ (self):
        return self.email