"""Main URL configuration. Each app has its own urls.py that is included here."""
from django.contrib import admin
from django.urls import include, path

from . import views

# Titles shown on the Django admin site.
admin.site.site_header = "QuestForge Administration"
admin.site.site_title = "QuestForge Admin"
admin.site.index_title = "Manage users, quests and achievements"

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("quests/", include("quests.urls")),
    path("achievements/", include("achievements.urls")),
    path("", include("reports.urls")),
    path("admin/", admin.site.urls),
]
