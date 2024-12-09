from django.contrib import admin
from .models import Service, Appointment, Vet
# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duration')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date', 'time_slot', 'status')

@admin.register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'is_available')
    list_editable = ('is_available',)