from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# XP a user earns for completing a quest of each difficulty.
XP_REWARDS = {
    "easy": 10,
    "medium": 25,
    "hard": 50,
    "epic": 100,
}


class Category(models.Model):
    """A shared list of categories (Study, Work, Health, ...). Staff manage it in the admin."""

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Quest(models.Model):
    """A goal that belongs to one user."""

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("epic", "Epic"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quests")
    # If a category is deleted, its quests stay and simply have no category.
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="quests"
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="easy")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    deadline = models.DateField(null=True, blank=True)
    # Filled in when the quest is completed. Stored, so editing the difficulty
    # later does not change XP that was already earned.
    xp_earned = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title

    @property
    def xp_reward(self):
        """XP this quest is worth, based on its difficulty."""
        return XP_REWARDS[self.difficulty]

    @property
    def is_completed(self):
        return self.status == "completed"

    @property
    def is_overdue(self):
        if self.deadline is None or self.is_completed:
            return False
        return self.deadline < timezone.localdate()

    def mark_complete(self, when=None):
        """Complete the quest and record the XP it earned."""
        self.status = "completed"
        self.completed_at = when or timezone.now()
        self.xp_earned = self.xp_reward
        self.save()
