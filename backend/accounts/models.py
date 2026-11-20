from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """Extra details for a user, and their daily streak.

    Django's built-in User already stores username, email and password,
    so this model only holds what User does not have.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    # Streak = number of days in a row on which the user completed a quest.
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def name(self):
        return self.display_name or self.user.username

    @property
    def streak_today(self):
        """The streak as it stands today. It shows 0 once a whole day is missed."""
        if self.last_active_date is None:
            return 0
        yesterday = timezone.localdate() - timedelta(days=1)
        if self.last_active_date < yesterday:
            return 0
        return self.current_streak

    def update_streak(self, day=None):
        """Record that the user completed a quest on `day` (default: today)."""
        day = day or timezone.localdate()

        if self.last_active_date and day <= self.last_active_date:
            return  # already counted this day

        if self.last_active_date == day - timedelta(days=1):
            self.current_streak += 1  # active yesterday too, so the streak grows
        else:
            self.current_streak = 1  # first quest ever, or a day was missed

        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_active_date = day
        self.save()
