from django.urls import path
from .views import update_profile

app_name = 'accounts'

urlpatterns = [
    path('update/', update_profile, name='update_profile'),
]
