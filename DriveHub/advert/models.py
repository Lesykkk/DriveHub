from django.db import models
from django.urls import reverse
from account.models import User


class Brand(models.model):
    value = models.CharField(max_length=50)

class Model(models.model):
    value = models.CharField(max_length=100)

class BodyType(models.model):
    value = models.CharField(max_length=50)

class FuelType(models.model):
    value = models.CharField(max_length=50)

class FuelConsumption(models.Model):
    city = models.DecimalField(max_digits=4, decimal_places=1)
    highway = models.DecimalField(max_digits=4, decimal_places=1)
    mixed = models.DecimalField(max_digits=4, decimal_places=1)

class DriveWheelType(models.model):
    value = models.CharField(max_length=50)

class TransmissionType(models.model):
    value = models.CharField(max_length=50)

class Color(models.model):
    value = models.CharField(max_length=50)

class TransportType(models.Model):
    value = models.CharField(max_length=50)


class Transport(models.Model):
    transport_type = models.ForeignKey(TransportType)
    brand = models.ForeignKey(Brand)
    model = models.ForeignKey(Model)
    year = models.PositiveSmallIntegerField()
    body_type = models.ForeignKey(BodyType)
    fuel_type = models.ForeignKey(FuelType)
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1)
    engine_power = models.models.PositiveSmallIntegerField()
    fuel_consumption = models.ForeignKey(FuelConsumption)
    drive_wheel_type = models.ForeignKey(DriveWheelType)
    transmission_type = models.ForeignKey(TransmissionType)
    color = models.ForeignKey(Color)
    mileage = models.PositiveIntegerField()
    owners_number = models.PositiveSmallIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"


class TransportPhoto(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='transports/%Y/%m/%d')


class Advert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adverts')
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
        return f"Advert for {self.transport.title} by {self.user.username}"

    def get_absolute_url(self):
        return reverse(':advert_detail', args=[self.slug])