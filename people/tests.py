from django.test import TestCase, Client
from people.views import *
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Doctor, Patient, Appointment
from .serializers import *
from django.contrib.auth.models import User

class DoctorViewSetTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password("testpassword")
        self.doctor = Doctor.objects.create(user_profile=self.user)
        self.serializer = DoctorSerializer(self.doctor)

    def test_get_queryset(self):
        queryset = DoctorViewSet.get_queryset(self)
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.doctor, queryset)

    def test_get(self):
        response = self.client.get('/doctors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.serializer.data])

class PatientViewSetTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.user.set_password("testpassword")
        self.patient = Patient.objects.create(user_profile=self.user)
        self.serializer = PatientSerializer(self.patient)

    def test_get_queryset(self):
        queryset = PatientViewSet.get_queryset(self)
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.patient, queryset)

    def test_get_for_patient(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'error': 'unauthorized'})

    def test_post(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'user': self.user.id,
            'can_login': True
        }

        response = self.client.post('/patients/', data=data)
        self.assertEqual(response.status_code, 401)

import json

class AppointmentViewSetTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='testuser')
        self.user.set_password("testpassword")
        self.user.save()
        self.doctor = Doctor.objects.create()
        self.patient = Patient(user_profile=self.user)
        self.patient.save()
        self.user.patient_profile = self.patient
        self.user.save()
        self.appointment = Appointment.objects.create(doctor=self.doctor, patient=self.patient,
                                                     start_time='2022-10-04T18:00:00Z', end_time='2022-10-04T19:00:00Z')
        self.serializer = AppointmentSerializer(self.appointment)
        

    def test_get_queryset(self):
        queryset = AppointmentViewSet.get_queryset(self)
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.appointment, queryset)


    def test_create_appointment(self):
        self.user.is_active = True
        self.user.save()
        
        if self.client.login(username='testuser', password='testpassword'):
            
            data = {
                    "doctor": 1,
                    "start_time": "2023-10-05T18:00:00Z",
                    "end_time": "2023-10-05T19:00:00Z",
                }
            
            response = self.client.post('/appointments/', data={**data})
            self.assertEqual(response.status_code, 201)