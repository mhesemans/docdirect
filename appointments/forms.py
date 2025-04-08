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
