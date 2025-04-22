from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('my-adverts/', views.my_adverts, name='my-adverts'),
    path('favourite/', views.favourite, name='favourite'),
    path('settings/', views.settings, name='settings'),
]