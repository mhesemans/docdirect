"""
Admin configuration for the appointments app.

Includes admin settings for:
- Appointment model
"""

from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin interface for the Appointment model.

    Enables viewing, searching, filtering, and managing
    appointments in the Django admin panel.
    """

    list_display = (
        'patient',
        'gp',
        'date',
        'time',
        'is_completed',
        'preferred_contact',
    )
    list_filter = (
        'gp',
        'date',
        'is_completed',
        'preferred_contact',
    )
    search_fields = (
        'patient__first_name',
        'patient__last_name',
        'gp__first_name',
        'gp__last_name',
        'reason_for_visit',
    )
    ordering = ('date', 'time')
