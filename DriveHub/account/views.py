from django.shortcuts import render

def login(request):
    return render(request, 'account/login.html')

def registration(request):
    return render(request, 'account/registration.html')

def my_adverts(request):
    return render(request, 'account/my-adverts.html')

def favourite(request):
    return render(request, 'account/favourite.html')

def settings(request):
    return render(request, 'account/settings.html')