from django import forms
from .models import Appointment, Vet

class AppointmentForm(forms.ModelForm):
    vet = forms.ModelChoiceField(queryset=Vet.objects.filter(is_available=True))


    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time_slot', 'vet']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
        }

class VetForm(forms.ModelForm):
    class Meta:
        model = Vet
        fields = ['specialty', 'bio', 'is_available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }