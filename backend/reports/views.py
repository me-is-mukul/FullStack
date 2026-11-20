import csv
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from quests.models import XP_REWARDS, Quest
from quests.utils import get_level_info, get_status_counts, get_total_xp

CHART_DAYS = 30
PLAYERS_PER_PAGE = 20


def get_leaderboard():
    """All active users with their total XP and completed quest count, best first."""
    completed = Q(quests__status="completed")
    return (
        User.objects.filter(is_active=True)
        .annotate(
            total_xp=Sum("quests__xp_earned", filter=completed, default=0),
            completed_count=Count("quests", filter=completed),
        )
        .order_by("-total_xp", "-completed_count", "username")
    )


@login_required
def dashboard(request):
    user = request.user
    my_quests = Quest.objects.filter(owner=user)

    context = {
        "level": get_level_info(get_total_xp(user)),
        "profile": user.profile,
        "counts": get_status_counts(user),
        "upcoming": my_quests.exclude(status="completed")
        .filter(deadline__isnull=False)
        .order_by("deadline", "id")[:5],
        "recently_completed": my_quests.filter(status="completed").order_by("-completed_at")[:5],
        "recent_achievements": user.achievements.select_related("achievement")[:3],
    }
    return render(request, "reports/dashboard.html", context)


@login_required
def my_reports(request):
    user = request.user
    my_quests = Quest.objects.filter(owner=user)

    # GROUP BY category: how many quests, how many completed, XP earned.
    by_category = (
        my_quests.values("category__name")
        .annotate(
            total=Count("id"),
            completed=Count("id", filter=Q(status="completed")),
            xp=Sum("xp_earned"),
        )
        .order_by("-total", "category__name")
    )

    # GROUP BY difficulty. The loop puts the rows in Easy -> Epic order and
    # adds a 0 row for any difficulty the user has not used yet.
    difficulty_rows = my_quests.values("difficulty").annotate(
        total=Count("id"), completed=Count("id", filter=Q(status="completed"))
    )
    counts_by_difficulty = {row["difficulty"]: row for row in difficulty_rows}
    by_difficulty = []
    for value, label in Quest.DIFFICULTY_CHOICES:
        row = counts_by_difficulty.get(value, {"total": 0, "completed": 0})
        by_difficulty.append({
            "label": label,
            "xp_each": XP_REWARDS[value],
            "total": row["total"],
            "completed": row["completed"],
        })

    # XP earned on each of the last 30 days. Days with no XP are filled with 0.
    today = timezone.localdate()
    first_day = today - timedelta(days=CHART_DAYS - 1)
    daily_rows = (
        my_quests.filter(status="completed", completed_at__date__gte=first_day)
        .annotate(day=TruncDate("completed_at"))
        .values("day")
        .annotate(xp=Sum("xp_earned"))
    )
    xp_per_day = {row["day"]: row["xp"] for row in daily_rows}
    days = [first_day + timedelta(days=i) for i in range(CHART_DAYS)]

    xp_chart = {
        "labels": [day.strftime("%d %b") for day in days],
        "values": [xp_per_day.get(day, 0) for day in days],
    }
    category_chart = {
        "labels": [row["category__name"] or "No category" for row in by_category],
        "total": [row["total"] for row in by_category],
        "completed": [row["completed"] for row in by_category],
    }

    context = {
        "level": get_level_info(get_total_xp(user)),
        "counts": get_status_counts(user),
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "xp_last_30_days": sum(xp_chart["values"]),
        "chart_days": CHART_DAYS,
        "xp_chart": xp_chart,
        "category_chart": category_chart,
    }
    return render(request, "reports/reports.html", context)


@login_required
def export_quests_csv(request):
    """Download the logged-in user's quests as a CSV file (opens in Excel)."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="my-quests.csv"'

    writer = csv.writer(response)
    writer.writerow(["Title", "Category", "Difficulty", "Status", "Deadline", "Created", "Completed", "XP earned"])

    quests = Quest.objects.filter(owner=request.user).select_related("category").order_by("created_at")
    for quest in quests:
        writer.writerow([
            quest.title,
            quest.category.name if quest.category else "",
            quest.get_difficulty_display(),
            quest.get_status_display(),
            quest.deadline or "",
            timezone.localtime(quest.created_at).strftime("%Y-%m-%d %H:%M"),
            timezone.localtime(quest.completed_at).strftime("%Y-%m-%d %H:%M") if quest.completed_at else "",
            quest.xp_earned,
        ])
    return response


@login_required
def leaderboard(request):
    players = get_leaderboard()
    page = Paginator(players, PLAYERS_PER_PAGE).get_page(request.GET.get("page"))

    # Position of the logged-in user in the full ranking.
    ranking = list(players.values_list("id", flat=True))
    my_rank = ranking.index(request.user.id) + 1 if request.user.id in ranking else None

    context = {
        "page": page,
        "rank_offset": page.start_index() - 1,  # so page 2 starts at rank 21
        "my_rank": my_rank,
    }
    return render(request, "reports/leaderboard.html", context)


@login_required
def staff_report(request):
    # Only staff accounts may see numbers about every user.
    if not request.user.is_staff:
        raise PermissionDenied

    quest_totals = Quest.objects.aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(status="completed")),
        xp=Sum("xp_earned", default=0),
    )
    completion_rate = 0
    if quest_totals["total"]:
        completion_rate = quest_totals["completed"] * 100 // quest_totals["total"]

    by_category = (
        Quest.objects.values("category__name")
        .annotate(total=Count("id"), completed=Count("id", filter=Q(status="completed")))
        .order_by("-total", "category__name")
    )

    week_ago = timezone.now() - timedelta(days=7)
    context = {
        "user_count": User.objects.filter(is_active=True).count(),
        "new_users": User.objects.filter(date_joined__gte=week_ago).count(),
        "quest_totals": quest_totals,
        "completion_rate": completion_rate,
        "by_category": by_category,
        "top_players": get_leaderboard()[:5],
        "newest_users": User.objects.order_by("-date_joined")[:5],
    }
    return render(request, "reports/staff_report.html", context)
