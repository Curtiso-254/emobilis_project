from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, Appointment, Vet
from .forms import AppointmentForm
from django.urls import reverse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io



def is_admin(user):
    return user.is_staff or user.is_superuser


#@user_passes_test(is_admin, login_url="/no-access")

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.vet = Vet.objects.get(pk=request.POST['vet'])
            appointment.save()
            return redirect(reverse_lazy('appointments:appointment_list'))  # Update this line
    else:
        form = AppointmentForm()
        vets = Vet.objects.filter(is_available=True)
    return render(request, 'appointments/appointment_form.html', {'form': form})


@login_required
def appointment_list(request):
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(client=request.user)
        return render(request, 'appointments/appointment_list.html', {'appointments': appointments})
    else:
        return get_object_or_404(Appointment, pk=-1)  # Return a dummy 404 response
    
def appointment_form_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
        vets = Vet.objects.filter(is_available=True)
        return render(request, 'appointments/appointment_form.html', {'form': form, 'vets': vets})


@user_passes_test(is_admin, login_url='/no-access/')
def manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/manage.html', {'appointments': appointments})

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'approved'
    appointment.save()
    send_appointment_email(appointment, 'approved')
    return redirect('appointments:manage_appointments')

@login_required
@user_passes_test(lambda u: u.is_staff)
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'canceled'
    appointment.save()
    send_appointment_email(appointment, 'canceled')
    return redirect('appointments:manage_appointments')

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('appointments:manage_appointments')

def send_appointment_email(appointment, status):
    subject = f'Your appointment has been {status}'
    message = f'Dear {appointment.client.username},\n\nYour appointment for {appointment.service.name} on {appointment.date} at {appointment.time_slot} has been {status}.\n\nThank you,\nGardenVet'
    recipient_list = [appointment.client.email]
    send_mail(subject, message, 'your-email@example.com', recipient_list)

@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_report(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    appointments = Appointment.objects.all()
    y = 750
    p.drawString(100, y, "Appointments Report")
    y -= 30

    for appointment in appointments:
        text = f"Service: {appointment.service.name}, Date: {appointment.date}, Time: {appointment.time_slot}, Client: {appointment.client.username}, Status: {appointment.status}"
        p.drawString(100, y, text)
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def vet_list(request):
    vets = Vet.objects.all()
    return render(request, 'appointments/vet_list.html', {'vets': vets})

def book_with_vet(request, vet_id):
    vet = get_object_or_404(Vet, id=vet_id)

    if not vet.is_available:
        #Redirect or show an error message
        return redirect('appointments:vet_list')
    
    if request.method == 'POST':
        form =AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.vet = vet # add this to associate a specific vet with an appointment
            appointment.save()
            return redirect('appointments:appointment_list')
        
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book_with_vet.html', {
        'form': form,
        'vet': vet
    })
