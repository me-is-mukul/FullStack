from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Achievement(models.Model):
    """A badge that unlocks when one of the user's numbers reaches a target.

    Example: metric="quests_completed", threshold=5 -> "Complete 5 quests".
    Staff can add new achievements from the admin site.
    """

    METRIC_CHOICES = [
        ("quests_completed", "Quests completed"),
        ("total_xp", "Total XP"),
        ("longest_streak", "Longest streak (days)"),
    ]

    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200)
    metric = models.CharField(max_length=20, choices=METRIC_CHOICES)
    threshold = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Links a user to an achievement they have unlocked (a many-to-many with extra data)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="unlocks")
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-unlocked_at", "-id"]
        # The same achievement cannot be unlocked twice by one user.
        constraints = [
            models.UniqueConstraint(fields=["user", "achievement"], name="unique_user_achievement")
        ]

    def __str__(self):
        return f"{self.user.username} unlocked {self.achievement.name}"
