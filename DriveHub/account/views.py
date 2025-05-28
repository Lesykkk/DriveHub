from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from .forms import AccountLoginForm, AccountRegistrationForm, ProfileForm
from advert.models import *

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
    else:
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html', {
        'form': form,
    })


@login_required
def my_ads(request):
    adverts_list = request.user.adverts.order_by('-id')
    paginator = Paginator(adverts_list, 5)
    page_number = request.POST.get('page', 1)
    adverts = paginator.get_page(page_number)
    return render(request, 'account/my-ads.html', {
        'user': request.user,
        'adverts': adverts,
    })


@login_required
def favourites(request):
    favourites_list = Advert.objects.filter(favourite__user=request.user).order_by('-id')
    paginator = Paginator(favourites_list, 5)
    page_number = request.POST.get('page', 1)
    adverts = paginator.get_page(page_number)
    return render(request, 'account/favourites.html', {
        'user': request.user,
        'adverts': adverts,
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


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('advert:home'))