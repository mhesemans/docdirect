from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm


@login_required
def update_profile(request):
    """
    Allows a logged-in user to update their personal information.

    **Context**
    ``form``: An instance of :form:`accounts.UserUpdateForm` pre-filled with current user data.

    **Template**
    :template:`accounts/update_profile.html`
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('accounts:update_profile')
    else:
        form = UserUpdateForm(instance=request.user, user=request.user)

    return render(request, 'accounts/update_profile.html', {'form': form})
