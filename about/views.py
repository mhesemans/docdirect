from django.shortcuts import render
from .models import StaffMember


def about_view(request):
    staff = StaffMember.objects.filter(status=1).order_by('name')  # only published
    return render(request, "about/about.html", {"staff": staff})
