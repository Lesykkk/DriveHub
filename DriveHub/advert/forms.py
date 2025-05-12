from django import forms
from .models import Transport, Advert, FuelConsumption


class FuelConsumptionForm(forms.ModelForm):
    class Meta:
        model = FuelConsumption
        fields = [
            'city_consumption',
            'highway_consumption',
            'mixed_consumption',
        ]


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = [
            'transport_type',
            'year',
            'body_type',
            'fuel_type',
            'engine_volume',
            'engine_power',
            'drive_type',
            'transmission_type',
            'color',
            'mileage',
            'owners_number',
        ]


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = [
            'price',
            'description',
        ]