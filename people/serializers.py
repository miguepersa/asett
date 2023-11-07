from rest_framework.serializers import ModelSerializer
from .models import *

class DoctorSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Doctor

class PatientSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Patient

class AppointmentSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Appointment
