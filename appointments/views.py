from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.timezone import now, make_aware
from datetime import date, time, datetime, timedelta
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.models import User


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


@login_required
def book_appointment(request):
    """
    Allows a logged-in user to book a new appointment with a selected GP and available time slots.

    Handles:
    - GET: Show the GP & date selector and, if both are provided, time slots.
    - POST: Save a valid appointment and redirect to patient overview.

    **Template**
    - appointments/book_appointment.html
    """
    from django.utils.timezone import now

    form = AppointmentForm()
    gps = User.objects.filter(groups__name="GP")
    selected_gp_id = request.GET.get("gp")
    selected_date = request.GET.get("date")
    available_slots = []
    today = date.today()

    # If GP and date are selected, calculate available time slots
    if selected_gp_id and selected_date:
        try:
            selected_gp = User.objects.get(id=selected_gp_id)
            selected_day = datetime.strptime(selected_date, "%Y-%m-%d").date()
            is_thursday = selected_day.weekday() == 3

            # Set time range
            start_time = time(8, 0)
            end_time = time(16, 0) if is_thursday else time(19, 0)
            slot = make_aware(datetime.combine(selected_day, start_time))
            now_plus_1h = now() + timedelta(hours=1)

            while slot.time() < end_time:
                # Skip lunch hour
                if not time(13, 0) <= slot.time() < time(14, 0):
                    # Ensure the slot is in the future by at least 1 hour
                    if slot > now_plus_1h:
                        slot_taken = Appointment.objects.filter(
                            date=selected_day, time=slot.time(), gp=selected_gp
                        ).exists()
                        if not slot_taken:
                            available_slots.append(slot.time())
                slot += timedelta(minutes=15)

        except (ValueError, User.DoesNotExist):
            messages.error(request, "Invalid GP or date selected.")

    # If the form is submitted via POST
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return redirect("appointments:patient_appointments")

    return render(request, "appointments/book_appointment.html", {
        "form": form,
        "gps": gps,
        "available_slots": available_slots,
        "selected_date": selected_date,
        "selected_gp_id": selected_gp_id,
        "today": today.isoformat()
    })
