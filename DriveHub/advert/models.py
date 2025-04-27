from django.db import models
from django.urls import reverse
from django.conf import settings


class Brand(models.Model):
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'brand' 


class Model(models.Model):
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'model' 


class BrandModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    class Meta:
        db_table = 'brand_model'
        unique_together = ('brand', 'model')


class BodyType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'body_type'


class FuelType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'fuel_type' 


class FuelConsumption(models.Model):
    city = models.DecimalField(max_digits=4, decimal_places=1)
    highway = models.DecimalField(max_digits=4, decimal_places=1)
    mixed = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        db_table = 'fuel_consumption' 


class DriveType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'drive_type'


class TransmissionType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'transmission_type'


class Color(models.Model):
    value = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'color'


class TransportType(models.Model):
    value = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'transport_type'


class Transport(models.Model):
    transport_type = models.ForeignKey(TransportType, on_delete=models.PROTECT)
    brand_model = models.ForeignKey(BrandModel, on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField()
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.PROTECT)
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1)
    engine_power = models.PositiveSmallIntegerField()
    fuel_consumption = models.ForeignKey(FuelConsumption, on_delete=models.PROTECT)
    drive_type = models.ForeignKey(DriveType, on_delete=models.PROTECT)
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    mileage = models.PositiveIntegerField()
    owners_number = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'transport'

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"
    
    def __repr__(self):
        return f"{self.brand} {self.model} {self.year}"


class TransportPhoto(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='transports/%Y/%m/%d')

    class Meta:
        db_table = 'transport_photo'


class Advert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adverts')
    transport = models.OneToOneField(Transport, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True)
    price = models.PositiveIntegerField()
    city = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'advert'
        # indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return f"Advert for {self.transport} by {self.user}"
    
    def __repr__(self):
        return f"Advert for {self.transport} by {self.user}"

    # def get_absolute_url(self):
    #     return reverse('advert:advert_detail', args=[self.slug])


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'favourites')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourite'