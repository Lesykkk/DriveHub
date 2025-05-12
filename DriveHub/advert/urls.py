from django.urls import path
from . import views

app_name = 'advert'

urlpatterns = [
    path('', views.home, name='home'),
    path('ajax/get-models/', views.get_models_by_brand, name='get-models-by-brand'),
    path('create/', views.create_advert, name='create-advert'),
    path('<slug:slug>/', views.advert_detail, name='advert-detail'),
]