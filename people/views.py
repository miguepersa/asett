from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from people.models import *
from people.serializers import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pytz

utc=pytz.UTC

# Create your views here.
class DoctorViewSet(APIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return Doctor.objects.all()

    def get(self, request):
        qs = self.get_queryset()
        return Response(self.serializer_class(qs, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # POST data
        data = request.data

        # User 
        u = User.objects.get(pk=data['user'])
        
        # New doctor instance
        doctor = Doctor(user_profile=u)
        doctor.save()

        # Returning the object that was just created
        return Response(self.serializer_class(doctor).data, status=status.HTTP_200_OK)


class PatientViewSet(APIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.all()

    def get(self, request):
        u = request.user
        
        # If doctor or patient
        if hasattr(u, "patient_profile") or hasattr(u, "doctor_profile"):
            return Response(self.serializer_class(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
        
        # If not an user nor a patient
        return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):

        # If user is doctor
        if not hasattr(request.user, "doctor_profile"):
            return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            
        # POST data
        data = request.data

        # User 
        u = User.objects.get(pk=data['user'])
        
        # If the user cannot login
        if not data['can_login']:
            u.is_active = False
            u.save()
        
        # New patient instance
        p = Patient(user_profile=u)
        p.save()
        return Response(self.serializer_class(p).data, status=status.HTTP_201_CREATED)


class AppointmentViewSet(APIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.all()

    def get(self, request):

        # If doctor
        if hasattr(request.user, "doctor_profile"):
            qs = self.get_queryset().filter(doctor=request.user.doctor_profile)
            data = self.serializer_class(qs, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        
        # If patient
        elif hasattr(request.user, "patient_profile"):
            qs = self.get_queryset().filter(patient=request.user.patient_profile)
            data = self.serializer_class(qs, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        
        # If not doctor nor patient
        else:
            return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        u = request.user

        patient_profile = getattr(u, 'patient_profile', None)

    
        # If the user is a patient
        if patient_profile is not None:
            
            data = {**request.data}

            for key in data.keys():
                if type(data[key]) == type(list()):
                    data[key] = data[key][0]

            # Getting the doctor object
            doctor = Doctor.objects.get(pk=data['doctor'][0])
            del data['doctor']

            if "test" in data.keys():
                del data["test"]

            # New appointment instance
            ap = Appointment(**data, doctor=doctor, patient=request.user.patient_profile)
            
            # Checking the appoinments of the doctor to confirm if doctor is available
            for a in Appointment.objects.filter(doctor=doctor):
                
                # If the doctor is not available
                if ((a.start_time.replace(tzinfo=utc) <= datetime.datetime.strptime(ap.start_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc) and a.end_time.replace(tzinfo=utc) >= datetime.datetime.strptime(ap.end_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc) ) or 
                    (datetime.datetime.strptime(ap.start_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc) <= a.start_time.replace(tzinfo=utc) and datetime.datetime.strptime(ap.end_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc) >= a.start_time.replace(tzinfo=utc)) or 
                    (datetime.datetime.strptime(ap.start_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc) <= a.end_time.replace(tzinfo=utc) and datetime.datetime.strptime(ap.end_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc) >= a.end_time.replace(tzinfo=utc))
                    ):
                    return Response({'error': 'the doctor is not available in that timespan'}, status=status.HTTP_400_BAD_REQUEST)
                
            ap.save()
            return Response(self.serializer_class(ap).data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)