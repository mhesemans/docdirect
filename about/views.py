from django.shortcuts import render, redirect
from django.contrib import messages
from .models import StaffMember
from .forms import ContactUsForm


def about_view(request):
    staff = StaffMember.objects.filter(status=1).order_by('name')
    form = ContactUsForm()

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Thank you! Your message has been received.")
            return redirect('/about/#pane-contact')

    return render(request, "about/about.html", {
        "staff": staff,
        "form": form
    })
