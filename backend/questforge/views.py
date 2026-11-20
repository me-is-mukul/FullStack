from django.shortcuts import redirect, render


def home(request):
    # Logged-in users don't need the landing page.
    if request.user.is_authenticated:
        return redirect("reports:dashboard")
    return render(request, "home.html")
