from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date of birth'
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Save date of birth to user profile
        profile = user.userprofile
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.save()

        return user


class UserUpdateForm(UserChangeForm):
    """
    A form that allows users to update their profile details.

    Includes fields from both :model:`auth.User` and :model:`accounts.UserProfile`.

    Fields:
    - first_name
    - last_name
    - email
    - date_of_birth
    - phone_number
    - next_of_kin
    - preferred_contact
    """

    password = None  # Hide the password field

    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    phone_number = forms.CharField(
        label='Phone Number',
        max_length=15,
        required=False
    )

    next_of_kin = forms.CharField(
        label='Next of Kin',
        max_length=100,
        required=False
    )

    preferred_contact = forms.ChoiceField(
        label='Preferred Contact Method',
        choices=UserProfile.CONTACT_PREFERENCE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.user:
            profile = self.user.userprofile
            self.fields['date_of_birth'].initial = profile.date_of_birth
            self.fields['phone_number'].initial = profile.phone_number
            self.fields['next_of_kin'].initial = profile.next_of_kin
            self.fields['preferred_contact'].initial = profile.preferred_contact

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit)
        if self.user:
            profile = self.user.userprofile
            profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            profile.phone_number = self.cleaned_data.get('phone_number')
            profile.next_of_kin = self.cleaned_data.get('next_of_kin')
            profile.preferred_contact = self.cleaned_data.get('preferred_contact')
            if commit:
                profile.save()
        return user
