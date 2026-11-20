from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Achievement, UserAchievement
from .utils import check_achievements, get_user_stats


@login_required
def achievement_list(request):
    # Picks up achievements that staff added after the user already qualified.
    check_achievements(request.user)

    stats = get_user_stats(request.user)
    unlocked = {
        item.achievement_id: item.unlocked_at
        for item in UserAchievement.objects.filter(user=request.user)
    }

    rows = []
    for achievement in Achievement.objects.all():
        value = min(stats.get(achievement.metric, 0), achievement.threshold)
        rows.append({
            "achievement": achievement,
            "unlocked_at": unlocked.get(achievement.id),
            "value": value,
            "percent": value * 100 // achievement.threshold,
        })

    context = {"rows": rows, "unlocked_count": len(unlocked)}
    return render(request, "achievements/achievement_list.html", context)
