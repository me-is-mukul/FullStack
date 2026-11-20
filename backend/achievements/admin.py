from django.contrib import admin

from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "metric", "threshold", "description")
    list_filter = ("metric",)
    search_fields = ("name",)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("user", "achievement", "unlocked_at")
    list_filter = ("achievement",)
    search_fields = ("user__username",)
