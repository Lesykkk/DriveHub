from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('my-ads/', views.my_ads, name='my-ads'),
    path('favourites/', views.favourites, name='favourites'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout')
]