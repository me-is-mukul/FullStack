from quests.models import Quest
from quests.utils import get_total_xp

from .models import Achievement, UserAchievement


def get_user_stats(user):
    """The numbers that achievements are checked against. Keys match Achievement.METRIC_CHOICES."""
    return {
        "quests_completed": Quest.objects.filter(owner=user, status="completed").count(),
        "total_xp": get_total_xp(user),
        "longest_streak": user.profile.longest_streak,
    }


def check_achievements(user):
    """Unlock every achievement the user now qualifies for and return the new ones."""
    stats = get_user_stats(user)
    already_unlocked = UserAchievement.objects.filter(user=user).values_list(
        "achievement_id", flat=True
    )

    new_achievements = []
    for achievement in Achievement.objects.exclude(id__in=already_unlocked):
        if stats.get(achievement.metric, 0) >= achievement.threshold:
            UserAchievement.objects.create(user=user, achievement=achievement)
            new_achievements.append(achievement)
    return new_achievements
