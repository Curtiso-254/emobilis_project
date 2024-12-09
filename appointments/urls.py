from django.urls import path
from . import views
from .views import appointment_form_view, appointment_list, approve_appointment, cancel_appointment, delete_appointment, manage_appointments

app_name = 'appointments'

urlpatterns = [
    path('create1/', views.create_appointment, name='create_appointment'),
    # Add other URL patterns for listing, updating, and deleting appointments
    path('list/', views.appointment_list, name='appointment_list'),
    path('appointment-form/', appointment_form_view, name='appointment_form'),
    path('manage/', manage_appointments, name='manage'),
    path('approve/<int:appointment_id>/', approve_appointment, name='approve_appointment'),
    path('cancel/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
    path('delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('vets/', views.vet_list, name='vet_list'),
    path('book-with-vet/<int:vet_id>/', views.book_with_vet, name='book_with_vet'),
]