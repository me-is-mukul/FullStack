from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, RegisterForm, UserUpdateForm


def register(request):
    if request.user.is_authenticated:
        return redirect("reports:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # the post_save signal also creates the Profile
            login(request, user)
            messages.success(request, "Welcome to QuestForge! Create your first quest to get started.")
            return redirect("reports:dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile = request.user.profile

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
        # Validation copies the typed values onto the objects, so reload the
        # saved values for the summary card on the left.
        request.user.refresh_from_db()
        profile.refresh_from_db()
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {"user_form": user_form, "profile_form": profile_form, "profile": profile}
    return render(request, "accounts/profile.html", context)
