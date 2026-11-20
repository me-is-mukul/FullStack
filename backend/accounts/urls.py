from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

# Login, logout and password change use Django's built-in views;
# we only give them our own templates.
urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path(
        "password/",
        auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"),
        name="password_change",
    ),
    path(
        "password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
