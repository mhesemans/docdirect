from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Home as root URL
    path('summernote/', include('django_summernote.urls')),
]
