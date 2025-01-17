from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import AccountLoginForm, AccountRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from SQLite.lib.database import Database as db


def login(request):
    if request.method == 'POST':
        form = AccountLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            account = auth.authenticate(username=username,
                                      password=password)
            if account:
                auth.login(request, account)
                return HttpResponseRedirect(reverse('main:adverts_list'))
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
            messages.success(request, f'{account.username}, Successful registration')
            return HttpResponseRedirect(reverse('account:login'))
    else:
        form = AccountRegistrationForm()
    return render(request, 'account/registration.html')



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('account:profile'))
    else:
        form = ProfileForm(instance=request.user)
    
    adverts = db().get_adverts(request.user.username)
    return render(request, 'account/profile.html',
                  {'form': form,
                   'adverts': adverts})


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:adverts_list'))