"""
URL configuration for the Accounts app.

Handles user-related functionality such as profile updates.
"""

from django.urls import path
from .views import update_profile

app_name = 'accounts'

urlpatterns = [
    path('update/', update_profile, name='update_profile'),
]
