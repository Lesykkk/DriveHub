from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    phone_validator = RegexValidator(
        regex=r'^\+380\d{9}$',
        message=_("Phone number must be entered in the format: '+380123456789'."),
    )

    letters_only_validator = RegexValidator(
        regex=r"^[^\W\d_]+(?:['\-]?[^\W\d_]+)*$",
        message=_("The field may include spaces, apostrophes, and hyphens."),
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

    first_name = models.CharField(
        _("first name"),
        max_length=150,
        validators=[MinLengthValidator(3), letters_only_validator],
        error_messages={
            "min_length": _("The field must contain at least 3 letters.")
        },
    )
    
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        validators=[MinLengthValidator(3), letters_only_validator],
        error_messages={
            "min_length": _("The field must contain at least 3 letters.")
        },
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]

    objects = CustomUserManager()
    
    class Meta:
        db_table = 'user'

    def __str__ (self):
        return f"{self.email}"
    
    def __repr__ (self):
        return f"<CustomUser: {self.email}>"