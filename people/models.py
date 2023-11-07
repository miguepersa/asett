from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Doctor(models.Model):
    user_profile = models.OneToOneField(User, related_name='doctor_profile', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.user_profile.first_name} {self.user_profile.last_name}"

class Patient(models.Model):
    user_profile = models.OneToOneField(User, related_name='patient_profile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user_profile.first_name} {self.user_profile.last_name}"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='appointments', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, related_name='appointments', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()