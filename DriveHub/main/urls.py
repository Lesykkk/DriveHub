from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.adverts_list, name='adverts_list'),
    path('create/', views.create_advert, name='create_advert'),
    path('delete/<slug:slug>', views.delete_advert, name='delete_advert'),
    path('<slug:slug>/', views.advert_detail, name='advert_detail'),
]