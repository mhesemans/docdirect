"""
URL configuration for the About app.

Maps the about page view to the root of the 'about/' URL path.
"""

from django.urls import path
from .views import about_view

app_name = 'about'

urlpatterns = [
    path('', about_view, name='about'),
]
