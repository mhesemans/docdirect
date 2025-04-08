from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # View for patients to see their upcoming appointments
    path(
        'my-appointments/',
        views.patient_appointments,
        name='patient_appointments'
    ),

    # View for GPs to see appointments assigned to them
    path(
        'gp-appointments/',
        views.gp_appointments,
        name='gp_appointments'
    ),

    # View for secretaries to manage all appointments
    path(
        'manage/',
        views.manage_appointments,
        name='manage_appointments'
    ),
]
