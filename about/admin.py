from django.contrib import admin
from .models import StaffMember
from django_summernote.admin import SummernoteModelAdmin


@admin.register(StaffMember)
class StaffMemberAdmin(SummernoteModelAdmin):
    list_display = ('name', 'role', 'status')
    list_filter = ('role', 'status')
    search_fields = ('name', 'role')
    summernote_fields = ('content',)
