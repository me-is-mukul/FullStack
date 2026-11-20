from django.urls import path

from . import views

app_name = "quests"

urlpatterns = [
    path("", views.quest_list, name="list"),
    path("new/", views.quest_create, name="create"),
    path("<int:pk>/", views.quest_detail, name="detail"),
    path("<int:pk>/edit/", views.quest_update, name="update"),
    path("<int:pk>/delete/", views.quest_delete, name="delete"),
    path("<int:pk>/start/", views.quest_start, name="start"),
    path("<int:pk>/complete/", views.quest_complete, name="complete"),
]
