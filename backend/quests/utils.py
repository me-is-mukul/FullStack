"""Small helpers for XP and levels, used by the quests, achievements and reports apps."""
from django.db.models import Count, Q, Sum

from .models import Quest

XP_PER_LEVEL = 100


def get_total_xp(user):
    """Total XP = sum of xp_earned over the user's completed quests."""
    result = Quest.objects.filter(owner=user, status="completed").aggregate(
        total=Sum("xp_earned", default=0)
    )
    return result["total"]


def get_level_info(total_xp):
    """Level 1 starts at 0 XP and every 100 XP is one more level."""
    level = total_xp // XP_PER_LEVEL + 1
    xp_into_level = total_xp % XP_PER_LEVEL
    return {
        "total_xp": total_xp,
        "level": level,
        "xp_into_level": xp_into_level,
        "xp_per_level": XP_PER_LEVEL,
        "xp_to_next": XP_PER_LEVEL - xp_into_level,
        "percent": xp_into_level * 100 // XP_PER_LEVEL,
    }


def get_status_counts(user):
    """How many of the user's quests are in each status, counted by the database."""
    return Quest.objects.filter(owner=user).aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status="pending")),
        in_progress=Count("id", filter=Q(status="in_progress")),
        completed=Count("id", filter=Q(status="completed")),
    )
