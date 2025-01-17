from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from .forms import AdvertForm
from .models import *
from SQLite.lib.database import Database as db

def adverts_list(request):
    sort_by = request.GET.get('sort_by', 'date_desc')
    transport_type = request.GET.get('transport_type', 'all')
    title = request.GET.get('title', '')
    year = request.GET.get('year', None)
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)

    if year and year.isdigit():
        year = int(year)
    else:
        year = 0
    
    if min_price and min_price.isdigit():
        min_price = int(min_price)
    else:
        min_price = 0
    
    if max_price and max_price.isdigit():
        max_price = int(max_price)
    else:
        max_price = 0

    adverts = db().get_adverts("", sort_by, transport_type, title, year, city, min_price, max_price)
    return render(request, 'main/index/index.html', {'adverts': adverts})

def advert_detail(request, slug):
    advert = db().get_advert_by_slug(slug)
    if advert is None:
        raise Http404()
    return render(request, 'main/advert/detail.html', {'advert': advert})

@login_required
def create_advert(request):
    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES)
        if form.is_valid():
            advert = form.save(commit=False)
            advert.account = request.user
            advert.save()
            return redirect(advert.get_absolute_url())
    else:
        form = AdvertForm()
    return render(request, 'main/advert/create.html', {'form': form})

@login_required
def delete_advert(request, slug):
    advert = get_object_or_404(Advert, slug=slug, account=request.user)
    advert.delete()
    messages.success(request, 'Advert was deleted successfully.')
    return HttpResponseRedirect(reverse('account:profile'))