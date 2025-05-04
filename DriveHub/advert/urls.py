from django.urls import path
from . import views

app_name = 'advert'

urlpatterns = [
    path('', views.home, name='home'),
    path('create-advert/', views.create_advert, name='create-advert'),
    path('ajax/get-models/', views.get_models_by_brand, name='get-models-by-brand'),
    path('advert-detail/', views.advert_detail, name='advert-detail'),
]
