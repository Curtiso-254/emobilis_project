from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text='Duration in minutes')

    def __str__(self):
        return self.name

class Vet(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        specialty = models.CharField(max_length=100)
        is_available = models.BooleanField(default=True)
        bio = models.TextField(blank=True, null=True)

        def __str__(self):
            return f"{self.user.first_name} {self.user.last_name}"

class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()
    vet = models.ForeignKey(Vet, on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled')
    ), default='pending')


    def __str__(self):
        return f"{self.client.username} - {self.service.name} ({self.date} {self.time_slot})"
    
   