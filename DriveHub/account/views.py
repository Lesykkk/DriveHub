from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import AccountLoginForm, AccountRegistrationForm
from django.contrib.auth.decorators import login_required
from advert.models import *


def login(request):
    if request.method == 'POST':
        form = AccountLoginForm(data=request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            email = request.POST['username']
            password = request.POST['password']
            account = auth.authenticate(username=email,
                                      password=password)
            if account:
                auth.login(request, account)
                next_url = request.POST.get('next') or reverse('advert:home')
                return redirect(next_url)
    else:
        form = AccountLoginForm()
    return render(request, 'account/login.html', {
        'form': form
    })


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
    return render(request, 'account/registration.html', {
        'form': form,
    })


@login_required
def my_ads(request):
    return render(request, 'account/my-ads.html', {
        'user': request.user,
        'my_ads': request.user.adverts.all(),
    })


@login_required
def favourites(request):
    favourites = Advert.objects.filter(favourite__user=request.user)
    return render(request, 'account/favourites.html', {
        'user': request.user,
        'favourites': favourites,
    })


@login_required
def settings(request):
    return render(request, 'account/settings.html')


def logout(request):
    auth.logout(request)
    return redirect(reverse('advert:home'))