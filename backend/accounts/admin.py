from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "current_streak", "longest_streak", "last_active_date")
    search_fields = ("user__username", "display_name")
