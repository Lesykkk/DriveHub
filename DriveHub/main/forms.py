from django import forms
from django.utils.text import slugify
from .models import Advert, Car, Truck, Boat


class AdvertForm(forms.ModelForm):
    TRANSPORT_CHOICES = [
        ('car', 'Car'),
        ('truck', 'Truck'),
        ('boat', 'Boat')
    ]

    transport_type = forms.ChoiceField(choices=TRANSPORT_CHOICES, required=True)
    
    title = forms.CharField(max_length=50, required=True)
    image = forms.ImageField(required=True)
    year = forms.IntegerField(required=True)
    engine_volume = forms.DecimalField(max_digits=4, decimal_places=2, required=True)
    mileage = forms.IntegerField(required=True)
    weight = forms.IntegerField(required=True)
    
    seat_number = forms.IntegerField(required=False)
    load_capacity = forms.IntegerField(required=False)
    propeller_number = forms.IntegerField(required=False)

    class Meta:
        model = Advert
        fields = ['price', 'city', 'description']

    def save(self, commit=True):
        transport_type = self.cleaned_data['transport_type']

        if transport_type == 'car':
            transport = Car.objects.create(
                title=self.cleaned_data['title'],
                image=self.cleaned_data['image'],
                year=self.cleaned_data['year'],
                engine_volume=self.cleaned_data['engine_volume'],
                mileage=self.cleaned_data['mileage'],
                weight=self.cleaned_data['weight'],
                seat_number=self.cleaned_data['seat_number'] or 5,
            )
        elif transport_type == 'truck':
            transport = Truck.objects.create(
                title=self.cleaned_data['title'],
                image=self.cleaned_data['image'],
                year=self.cleaned_data['year'],
                engine_volume=self.cleaned_data['engine_volume'],
                mileage=self.cleaned_data['mileage'],
                weight=self.cleaned_data['weight'],
                load_capacity=self.cleaned_data['load_capacity'] or 0,
            )
        elif transport_type == 'boat':
            transport = Boat.objects.create(
                title=self.cleaned_data['title'],
                image=self.cleaned_data['image'],
                year=self.cleaned_data['year'],
                engine_volume=self.cleaned_data['engine_volume'],
                mileage=self.cleaned_data['mileage'],
                weight=self.cleaned_data['weight'],
                propeller_number=self.cleaned_data['propeller_number'] or 1,
            )

        advert = super().save(commit=False)
        advert.transport = transport

        if not advert.slug:
            base_slug = slugify(transport.title)
            slug = base_slug
            counter = 1
            while Advert.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            advert.slug = slug

        if commit:
            advert.save()
        return advert
