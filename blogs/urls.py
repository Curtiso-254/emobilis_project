from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),

]