from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    """
    Represents a medical appointment between a patient and a GP.

    Includes details about the date, time, reason, and contact preferences.

    Related to:
    - :model:`auth.User` as both patient and GP.
    """

    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]

    patient = models.ForeignKey(
        User,
        related_name='appointments',
        on_delete=models.CASCADE
    )
    gp = models.ForeignKey(
        User,
        related_name='appointments_as_gp',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    time = models.TimeField()
    reason_for_visit = models.TextField()
    notes = models.TextField(blank=True)
    preferred_contact = models.CharField(
        max_length=10,
        choices=CONTACT_METHOD_CHOICES
    )
    is_completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        """
        Return a readable string representation of the appointment.
        """
        return f"{self.patient.get_full_name()} - {self.date} at {self.time}"
