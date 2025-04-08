from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date
from .models import Appointment
from .forms import AppointmentForm


def is_gp(user):
    """Check if the user belongs to the GP group."""
    return user.groups.filter(name="GP").exists()


def is_administrative(user):
    """Check if the user belongs to the Administrative Staff group."""
    return user.groups.filter(name="Administrative Staff").exists()


@login_required
def patient_appointments(request):
    """
    View to display upcoming appointments for the logged-in patient.

    **Context**
    - appointments: List of upcoming appointments for the user.

    **Template**
    - appointments/patient_appointments.html
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
    - appointments: List of upcoming and incomplete appointments for the GP.

    **Template**
    - appointments/gp_appointments.html
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
@user_passes_test(is_administrative)
def manage_appointments(request):
    """
    View to allow administrative staff to manage all appointments.

    **Context**
    - appointments: List of all upcoming appointments.

    **Template**
    - appointments/administrative_appointments.html
    """
    appointments = Appointment.objects.filter(
        date__gte=date.today()
    ).order_by("date", "time")

    return render(request, "appointments/administrative_appointments.html", {
        "appointments": appointments
    })


@login_required
@user_passes_test(is_gp)
def mark_completed(request, appointment_id):
    """
    Allows GPs to update notes and mark appointments as completed.

    Only the assigned GP can update their own appointments.

    **Context**
    - Updates `notes` and `is_completed` for a specific :model:`appointments.Appointment`

    **Redirect**
    - Redirects to `appointments:gp_appointments` after saving
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.gp:
        messages.error(request, "You are not authorized to modify this appointment.")
        return redirect("appointments:gp_appointments")

    if request.method == "POST":
        appointment.notes = request.POST.get("notes", "")
        appointment.is_completed = bool(request.POST.get("is_completed"))
        appointment.save()
        messages.success(request, "Appointment updated successfully.")

    return redirect("appointments:gp_appointments")
