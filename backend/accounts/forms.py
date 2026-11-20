from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    """Django's sign-up form (username + two passwords) with a required email added."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class UserUpdateForm(forms.ModelForm):
    """The parts of the User record a person may change themselves."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        others = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if others.exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 3})}
