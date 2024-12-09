from django.urls import path
from . import views
from mpesa.views import initiate_payment, mpesa_callback

#urlpatterns = [
urlpatterns = [
    path('pay/', views.mpesa_payment_page, name='payment_page'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
]