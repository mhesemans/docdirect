from django.contrib import admin
from django.urls import path, include


urlpatterns = [ 
    path('about/', include('about.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),  # Home as root URL
    path('summernote/', include('django_summernote.urls')),
]
