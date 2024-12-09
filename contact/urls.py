from django.urls import path, include
from . import views

urlpatterns = [

    path('contact/', views.contact, name='contact'),
    path('hello', views.say_hello),
    
]