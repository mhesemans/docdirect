"""
URL configuration for the appointments app.

Defines routes for patients, GPs, and administrative staff
to view and manage appointment-related tasks.
"""

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

    # View for patients to book a new appointment
    path(
        'book/',
        views.book_appointment,
        name='book_appointment'
    ),

    # View for GPs to see appointments assigned to them
    path(
        'gp-appointments/',
        views.gp_appointments,
        name='gp_appointments'
    ),

    # View for administrative staff to manage all appointments
    path(
        'manage/',
        views.manage_appointments,
        name='manage_appointments'
    ),

    # View for GPs to mark an appointment as completed
    path(
        'mark-completed/<int:appointment_id>/',
        views.mark_completed,
        name='mark_completed'
    ),

    # Edit an appointment (admin staff only)
    path(
        'edit/<int:appointment_id>/',
        views.edit_appointment,
        name='edit_appointment'
    ),
]
