from django.contrib import admin
from .models import StaffMember, ContactUs
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html


@admin.register(StaffMember)
class StaffMemberAdmin(SummernoteModelAdmin):
    list_display = ('name', 'role', 'status', 'image_preview')
    list_filter = ('role', 'status')
    search_fields = ('name', 'role')
    summernote_fields = ('content',)

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:4px;" />',
                obj.featured_image.url
            )
        return "-"
    image_preview.short_description = 'Image'


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'read', 'responded', 'contact_number')
    list_filter = ('read', 'responded')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'contact_number', 'subject', 'message')
