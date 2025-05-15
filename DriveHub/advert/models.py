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
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_models')
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
    city_consumption = models.DecimalField(max_digits=4, decimal_places=1)
    highway_consumption = models.DecimalField(max_digits=4, decimal_places=1)
    mixed_consumption = models.DecimalField(max_digits=4, decimal_places=1)

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
    fuel_consumption = models.OneToOneField(FuelConsumption, on_delete=models.PROTECT)
    drive_type = models.ForeignKey(DriveType, on_delete=models.PROTECT)
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    mileage = models.PositiveIntegerField()
    owners_number = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'transport'

    def __str__(self):
        return f"{self.brand_model.brand.value} {self.brand_model.model.value} {self.year}"
    
    def __repr__(self):
        return f"<Transport: {self.brand_model.brand.value} {self.brand_model.model.value} {self.year}>"


class TransportPhoto(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='transports/%Y/%m/%d')

    class Meta:
        db_table = 'transport_photo'


class Region(models.Model):
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'region'
        ordering = ['value']
  

class City(models.Model):
    value =  models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'city'
        ordering = ['value']


class RegionCity(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region_cities')
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        db_table = 'region_city'
        unique_together = ('region', 'city')


class Advert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adverts')
    transport = models.OneToOneField(Transport, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=50, unique=True)
    price = models.PositiveIntegerField()
    region_city = models.ForeignKey(RegionCity, on_delete=models.PROTECT)
    description = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'advert'
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return f"Advert for {self.transport} by {self.user}"
    
    def __repr__(self):
        return f"<Advert: {self.transport} {self.user}>"

    def get_absolute_url(self):
        return reverse('advert:advert-detail', args=[self.slug])


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'favourites')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourite'
        unique_together = ('user', 'advert')