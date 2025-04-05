from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


# Define an inline admin descriptor for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


# Define a new User admin with the inline profile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register User with the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
