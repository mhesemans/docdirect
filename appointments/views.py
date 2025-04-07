from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from datetime import date


def is_gp(user):
    return user.groups.filter(name="GP").exists()


def is_secretary(user):
    return user.groups.filter(name="Administrative Staff").exists()


@login_required
def patient_appointments(request):
    """
    View to display upcoming appointments for the logged-in patient.

    **Context**
    ``appointments``: List of upcoming appointments for the user.

    **Template**
    :template:`appointments/patient_appointments.html`
    """
    appointments = Appointment.objects.filter(
        patient=request.user,
        date__gte=date.today(),
        is_completed=False
    ).order_by("date", "time")

    return render(request, "appointments/patient_appointments.html", {
        "appointments": appointments
    })


@login_required
@user_passes_test(is_gp)
def gp_appointments(request):
    """
    View to display all appointments assigned to the logged-in GP.

    **Context**
    ``appointments``: List of upcoming and incomplete appointments for the GP.

    **Template**
    :template:`appointments/gp_appointments.html`
    """
    appointments = Appointment.objects.filter(
        gp=request.user,
        date__gte=date.today(),
        is_completed=False
    ).order_by("date", "time")

    return render(request, "appointments/gp_appointments.html", {
        "appointments": appointments
    })


@login_required
@user_passes_test(is_secretary)
def manage_appointments(request):
    """
    View to allow administrative staff to manage all appointments.

    **Context**
    ``appointments``: List of all upcoming appointments.

    **Template**
    :template:`appointments/manage_appointments.html`
    """
    appointments = Appointment.objects.filter(
        date__gte=date.today()
    ).order_by("date", "time")

    return render(request, "appointments/manage_appointments.html", {
        "appointments": appointments
    })
