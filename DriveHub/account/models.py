from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    phone_validator = RegexValidator(
                regex=r'^\+380\d{9}$',
                message=_("Phone number must be entered in the format: '+380123456789'. Up to 15 digits allowed."),
            )
    
    only_letters_unicode = RegexValidator(
        # regex=r'^[^\W\d_]+(?:[\s\'’-][^\W\d_]+)*$',
        regex=r'^(?=(?:.*[^\W\d_]){3,})[^\W\d_]+(?:[\s\'’-][^\W\d_]+)*$',
        message=_("The field must contain at least 3 letters and may include spaces, apostrophes, and hyphens.")
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



    first_name = models.CharField(_("first name"), max_length=150, validators=[only_letters_unicode])
    last_name = models.CharField(_("last name"), max_length=150, validators=[only_letters_unicode])
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]

    objects = CustomUserManager()
    
    class Meta:
        db_table = 'user'

    def __str__ (self):
        return f"{self.email}"
    
    def __repr__ (self):
        return f"<CustomUser: {self.email}>"