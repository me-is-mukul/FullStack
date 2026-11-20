from django.contrib import admin

from .models import Category, Quest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "difficulty", "status", "deadline", "xp_earned")
    list_filter = ("status", "difficulty", "category")
    search_fields = ("title", "owner__username")
    # XP is only given by the Complete button, so staff can see it but not edit it.
    readonly_fields = ("xp_earned", "created_at", "completed_at")
