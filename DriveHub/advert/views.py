from django.shortcuts import render

# Create your views here.
def advert(request):
    return render(request, 'advert/advert.html')