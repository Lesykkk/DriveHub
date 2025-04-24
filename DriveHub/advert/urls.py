from django.urls import path
from . import views

app_name = 'advert'

urlpatterns = [
    path('', views.home, name='home'),
]