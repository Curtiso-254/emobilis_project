from django.urls import path
from . import views
from .views import register_view, login_view

app_name = 'accounts'

urlpatterns = [
    path('register/',register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
]