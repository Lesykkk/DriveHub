from django.urls import path
from . import views

app_name = 'advert'

urlpatterns = [
    path('', views.home, name='home'),
    path('ajax/get-models/', views.get_models_by_brand, name='get-models-by-brand'),
    path('ajax/get-cities/', views.get_cities_by_region, name='get-cities-by-region'),
    path('ajax/toggle-favourite/', views.toggle_favourite, name='toggle-favourite'),
    path('create/', views.create_advert, name='create-advert'),
    path('delete/<int:advert_id>/', views.delete_advert, name='delete-advert'),
    path('advanced-filters/', views.advanced_filters, name='advanced-filters'),
    path('<slug:slug>/', views.advert_detail, name='advert-detail'),
]