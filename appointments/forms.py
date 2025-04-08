from django import forms
from django.contrib.auth.models import User
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """
    A form for creating or updating :model:`appointments.Appointment`.

    Dynamically filters GP field to users in the 'GP' group
    and displays full name (capitalized) in the dropdown.
    """

    gp = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="GP"),
        label="Select a Doctor",
        widget=forms.Select(attrs={"class": "form-select"}),
        to_field_name="id"
    )

    class Meta:
        model = Appointment
        fields = [
            'gp',
            'date',
            'time',
            'reason_for_visit',
            'notes',
            'preferred_contact',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason_for_visit': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'preferred_contact': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Capitalize GP names in the dropdown
        self.fields['gp'].label_from_instance = lambda obj: f"{obj.first_name.title()} {obj.last_name.title()}"


class AppointmentEditForm(forms.ModelForm):
    """
    A form used by administrative staff to edit or cancel appointments.

    Fields:
    - gp: doctor assigned to the appointment
    - date: appointment date
    - time: appointment time
    - is_completed: checkbox to mark as cancelled or done
    """

    gp = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="GP"),
        label="Assign GP",
        widget=forms.Select(attrs={"class": "form-select"}),
        to_field_name="id"
    )

    class Meta:
        model = Appointment
        fields = ['gp', 'date', 'time', 'is_completed']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gp'].label_from_instance = lambda obj: f"{obj.first_name.title()} {obj.last_name.title()}"
