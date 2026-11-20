from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reports/", views.my_reports, name="reports"),
    path("reports/export/", views.export_quests_csv, name="export"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("staff/", views.staff_report, name="staff"),
]
