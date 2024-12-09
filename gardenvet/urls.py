"""
URL configuration for gardenvet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from appointments import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mpesa/', include('mpesa.urls')),
    path('', include('pages.urls')),
    path('', include('products.urls')),
    path('', include('blogs.urls')),
    path('', include('accounts.urls')),
    #path('', views.home, name='home'),
    path('', include('contact.urls')),
   #path('pay/', views.pay_view, name='Pay'),
    path('', include('appointments.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('appointments/', include('appointments.urls', namespace='appointment')),
    path('no-access/', TemplateView.as_view(template_name='no_access.html'), name='no_access'),
    path('approve/<int:appointment_id>/appointments/manage/', views.approve_appointment, name='approve_appointment'),
    path('cancel/<int:appointment_id>/appointments/manage/', views.cancel_appointment, name='cancel_appointment'),
    path('delete/<int:appointment_id>/appointments/manage/', views.delete_appointment, name='delete_appointment'),



    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
