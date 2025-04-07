"""
URL configuration for the DocDirect project.

Includes all route definitions for each app.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # About page
    path('about/', include('about.urls'), name='about'),

    # News app (includes named routes like 'post_news')
    path('news/', include(('news.urls', 'news'), namespace='news')),

    # Admin and auth
    path('admin/', admin.site.urls),
    path('accounts/auth/', include('allauth.urls')),

    # User profile
    path('accounts/', include('accounts.urls')),

    # WYSIWYG editor
    path('summernote/', include('django_summernote.urls')),

    # Homepage
    path('', include('home.urls'), name='home'),
]
