from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib.auth import update_session_auth_hash
from .forms import AccountLoginForm, AccountRegistrationForm, ProfileForm
from advert.models import *

@login_not_required
def login(request):
    if request.method == 'POST':
        form = AccountLoginForm(data=request.POST)
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
            next_url = request.POST.get('next') or reverse('advert:home')
            return redirect(next_url)
            # return HttpResponseRedirect(reverse('advert:home'))
    else:
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html', {
        'form': form,
    })


@login_required
def my_ads(request):
    return render(request, 'account/my-ads.html', {
        'user': request.user,
        'adverts': request.user.adverts.all(),
    })


@login_required
def favourites(request):
    favourites = Advert.objects.filter(favourite__user=request.user)
    return render(request, 'account/favourites.html', {
        'user': request.user,
        'adverts': favourites,
    })


@login_required
def settings(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('account:settings')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'account/settings.html', {'form': form})



def logout(request):
    auth.logout(request)
    return redirect(reverse('advert:home'))