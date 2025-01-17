from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import *


@admin.register(Transport)
class TransportAdmin(PolymorphicParentModelAdmin):
    base_model = Transport
    child_models = [Car, Truck, Boat]
    list_display = ['title', 'polymorphic_ctype']
    list_filter = [PolymorphicChildModelFilter]


@admin.register(Car)
class CarAdmin(PolymorphicChildModelAdmin):
    base_model = Car
    list_display = ['title', 'engine_volume', 'mileage', 'weight', 'year', 'seat_number']


@admin.register(Truck)
class TruckAdmin(PolymorphicChildModelAdmin):
    base_model = Truck
    list_display = ['title', 'engine_volume', 'mileage', 'weight', 'year', 'load_capacity']


@admin.register(Boat)
class BoatAdmin(PolymorphicChildModelAdmin):
    base_model = Boat
    list_display = ['title', 'engine_volume', 'mileage', 'weight', 'year', 'propeller_number']


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ['account', 'transport', 'price', 'city', 'created', 'updated']
    list_select_related = ['transport', 'account']
    search_fields = ['city', 'account__username', 'transport__title']
    ordering = ['-created']