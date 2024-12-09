from django.shortcuts import render
from .forms import ContactForm
from django.shortcuts import render, redirect
# Create your views here

def home(request):
    return render(request, 'pages/home.html')

def base(request):
    return render(request, 'pages/base.html')

def service_view(request):
    return render(request, 'pages/service.html')

def about_us_view(request):
    return render(request, 'pages/about_us.html')


