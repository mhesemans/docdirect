from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """
    A form for creating or updating :model:`appointments.Appointment`.

    **Fields**
    - patient
    - gp
    - date
    - time
    - reason_for_visit
    - notes
    - preferred_contact
    - is_completed
    """

    class Meta:
        model = Appointment
        fields = [
            'patient',
            'gp',
            'date',
            'time',
            'reason_for_visit',
            'notes',
            'preferred_contact',
            'is_completed',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason_for_visit': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
