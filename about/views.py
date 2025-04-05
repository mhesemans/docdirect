from django.shortcuts import render, redirect
from django.contrib import messages
from .models import StaffMember
from .forms import ContactUsForm
from django.core.mail import send_mail


def about_view(request):
    staff = StaffMember.objects.filter(status=1).order_by('name')
    form = ContactUsForm()

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Thank you! Your message has been received.")
            # Send email to clinic (or test email)
            send_mail(
                subject=f"New Contact Message from {form.cleaned_data['name']}",
                message=(
                    f"Name: {form.cleaned_data['name']}\n"
                    f"Email: {form.cleaned_data['email']}\n"
                    f"Phone: {form.cleaned_data['contact_number']}\n"
                    f"Subject: {form.cleaned_data['subject']}\n\n"
                    f"Message:\n{form.cleaned_data['message']}"
                ),
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=['admin@docdirect.ie'],  # change to real email later
            )
            return redirect('/about/#pane-contact')

    return render(request, "about/about.html", {
        "staff": staff,
        "form": form
    })
