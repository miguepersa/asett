from rest_framework.routers import DefaultRouter
from people.views import *
from django.urls import path

app_name = "people"

urlpatterns = [
    path('doctors/', DoctorViewSet.as_view(), name="doctors"),
    path('patients/', PatientViewSet.as_view(), name="patients"),
    path('appointments/', AppointmentViewSet.as_view(), name="appointments"),
]

# router = DefaultRouter()
# router.register(r'doctors', DoctorViewSet)
# router.register(r'patients', PatientViewSet )
# router.register(r'appointments', AppointmentViewSet)