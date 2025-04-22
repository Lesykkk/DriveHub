from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=20)
    email = models.models.EmailField(_("email address"), max_length=254, unique = True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__ (self):
        return self.email