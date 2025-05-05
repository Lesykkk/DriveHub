from django import forms
from .models import Advert, Transport, TransportPhoto

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['price', 'city', 'description']

class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        exclude = []  

class TransportPhotoForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = TransportPhoto
        fields = ['image']
