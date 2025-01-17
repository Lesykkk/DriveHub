from polymorphic.models import PolymorphicModel
from django.db import models
from django.urls import reverse
from account.models import Account
    

class Transport(PolymorphicModel):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='transports/%Y/%m/%d')
    engine_volume = models.DecimalField(max_digits=4, decimal_places=1)
    mileage = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    year = models.PositiveIntegerField()


    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['title']),
        ]


    def __str__(self):
        return self.title
    


class Car(Transport):
    seat_number = models.PositiveIntegerField()


class Truck(Transport):
    load_capacity = models.PositiveIntegerField()


class Boat(Transport):
    propeller_number = models.PositiveIntegerField()


class Advert(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='adverts')
    transport = models.OneToOneField(Transport, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True)
    price = models.PositiveIntegerField()
    city = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return f"Advert for {self.transport.title} by {self.account.username}"

    def get_absolute_url(self):
        return reverse('main:advert_detail', args=[self.slug])