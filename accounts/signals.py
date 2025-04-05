from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile


@receiver(post_save, sender=User)
def handle_user_creation(sender, instance, created, **kwargs):
    if created:
        # Create user profile
        UserProfile.objects.create(user=instance)

        # Send welcome email
        subject = 'Welcome to DocDirect!'
        message = f"Hi {instance.first_name},\n\nThanks for registering with DocDirect. We're glad to have you!"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )
