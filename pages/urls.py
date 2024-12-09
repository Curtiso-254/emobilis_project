from django.urls import path
from . import views
from .views import service_view, about_us_view

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', service_view, name='services'),
    path('about-us/', about_us_view, name='about_us'),
]