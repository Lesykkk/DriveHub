from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import AccountLoginForm, AccountRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from advert.models import *


@login_required
def settings(request):
    return render(request, 'account/settings.html')


def login(request):
    if request.method == 'POST':
        form = AccountLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            account = auth.authenticate(email=email,
                                      password=password)
            if account:
                auth.login(request, account)
                return HttpResponseRedirect(reverse('advert:home'))
    else:
        form = AccountLoginForm()
    return render(request, 'account/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = AccountRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            account = form.instance
            auth.login(request, account)
            messages.success(request, f'{account.email}, Successful registration')
            return HttpResponseRedirect(reverse('account:login'))
    else:
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html')



@login_required
def my_adverts(request):
    
    User = get_user(request)
    print(User)
    adverts = Advert.objects.filter(user=request.user)

    
    print(adverts[0].description)
    return render(request, 'account/my-adverts.html',
                  {'adverts': adverts})

@login_required
def favourite(request):
    user = request.user

    liked_adverts = Advert.objects.filter(liked__user=user) 
    print(liked_adverts[0].price)

    return render(request, 'account/favourite.html', {
        'favourite_adverts': liked_adverts
    })


def logout(request):
    auth.logout(request)
    return redirect(reverse('advert:home'))