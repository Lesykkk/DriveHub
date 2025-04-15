from django.urls import path
from . import views

app_name = 'advert'


urlpatterns = [
    path('', views.advert, name='home'),
]