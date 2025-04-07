from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends the built-in Django User model with additional profile information.

    Fields:
    - user: One-to-one link to the Django User.
    - date_of_birth: Optional birthdate field.
    - phone_number: Optional contact number.
    - next_of_kin: Optional emergency contact.
    - preferred_contact: Choice field for contact preference (email or phone).
    """

    CONTACT_PREFERENCE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    next_of_kin = models.CharField(max_length=100, blank=True)
    preferred_contact = models.CharField(
        max_length=10,
        choices=CONTACT_PREFERENCE_CHOICES,
        default='email'
    )

    def __str__(self):
        return self.user.get_full_name()
