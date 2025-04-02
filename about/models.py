from django.db import models
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))

ROLE_CHOICES = [
    ('GP', 'General Practitioner'),
    ('NURSE', 'Nurse'),
    ('ADMIN', 'Administrative Staff'),
    ('OTHER', 'Other'),
]


class StaffMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ADMIN')
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"
