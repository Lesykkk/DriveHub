from django.shortcuts import render

def login(request):
    return render(request, 'account/login.html')

def registration(request):
    return render(request, 'account/registration.html')