from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render

def contact(request):
    if request.method == 'GET':
        return render(request, 'contact/contact.html')
    
    # Handle form submission
    # ...



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send the email using Django's send_mail function
        
        send_mail(
            "Contact Information",
            "Hello, your message has been received and is being looked at.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
)
        messages.success(request, f"Thank you for contacting us, {name}!")
        return redirect('contact')

    return render(request, 'contact/contact.html')


def say_hello(request):
    header = "welcome message"
    username = "Fundraisser"
    message = f"Hi, {username} you are welcome"


    send_mail(
    header,
    message,
        ["thekemist23@gmail.com"],
        ["iceking241@gmail.com"],
        fail_silently=False,
)