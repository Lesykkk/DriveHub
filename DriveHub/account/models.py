from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)


    class Meta:
        db_table = 'account';


    def __str__(self):
        return self.username