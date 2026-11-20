from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from achievements.utils import check_achievements

from .forms import QuestForm
from .models import Category, Quest
from .utils import get_level_info, get_status_counts, get_total_xp

QUESTS_PER_PAGE = 10

SORT_OPTIONS = {
    "newest": ["-created_at", "-id"],
    "oldest": ["created_at", "id"],
    "deadline": [F("deadline").asc(nulls_last=True), "-id"],
    "title": ["title", "id"],
}


@login_required
def quest_list(request):
    # Start from the logged-in user's quests only.
    quests = Quest.objects.filter(owner=request.user).select_related("category")

    # Search, filter and sort values come from the URL, e.g. ?q=report&status=pending
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    category = request.GET.get("category", "")
    difficulty = request.GET.get("difficulty", "")
    sort = request.GET.get("sort", "newest")
    if sort not in SORT_OPTIONS:
        sort = "newest"

    if query:
        quests = quests.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if status:
        quests = quests.filter(status=status)
    if category.isdigit():
        quests = quests.filter(category_id=category)
    if difficulty:
        quests = quests.filter(difficulty=difficulty)
    quests = quests.order_by(*SORT_OPTIONS[sort])

    page = Paginator(quests, QUESTS_PER_PAGE).get_page(request.GET.get("page"))

    context = {
        "page": page,
        "counts": get_status_counts(request.user),
        "categories": Category.objects.all(),
        "status_choices": Quest.STATUS_CHOICES,
        "difficulty_choices": Quest.DIFFICULTY_CHOICES,
        "query": query,
        "status": status,
        "category": category,
        "difficulty": difficulty,
        "sort": sort,
        "is_filtered": bool(query or status or category or difficulty),
    }
    return render(request, "quests/quest_list.html", context)


@login_required
def quest_detail(request, pk):
    # owner=request.user means another user's quest gives a 404.
    quest = get_object_or_404(Quest, pk=pk, owner=request.user)
    return render(request, "quests/quest_detail.html", {"quest": quest})


@login_required
def quest_create(request):
    if request.method == "POST":
        form = QuestForm(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.owner = request.user
            quest.save()
            messages.success(request, "Quest created.")
            return redirect("quests:detail", pk=quest.pk)
    else:
        form = QuestForm()
    return render(request, "quests/quest_form.html", {"form": form, "title": "New quest"})


@login_required
def quest_update(request, pk):
    quest = get_object_or_404(Quest, pk=pk, owner=request.user)
    if request.method == "POST":
        form = QuestForm(request.POST, instance=quest)
        if form.is_valid():
            form.save()
            messages.success(request, "Quest updated.")
            return redirect("quests:detail", pk=quest.pk)
    else:
        form = QuestForm(instance=quest)
    context = {"form": form, "quest": quest, "title": "Edit quest"}
    return render(request, "quests/quest_form.html", context)


@login_required
def quest_delete(request, pk):
    quest = get_object_or_404(Quest, pk=pk, owner=request.user)
    if request.method == "POST":
        quest.delete()
        messages.success(request, "Quest deleted.")
        return redirect("quests:list")
    return render(request, "quests/quest_confirm_delete.html", {"quest": quest})


@login_required
@require_POST
def quest_start(request, pk):
    quest = get_object_or_404(Quest, pk=pk, owner=request.user)
    if quest.status == "pending":
        quest.status = "in_progress"
        quest.save()
        messages.success(request, "Quest started. Good luck!")
    return redirect("quests:detail", pk=quest.pk)


@login_required
@require_POST
def quest_complete(request, pk):
    quest = get_object_or_404(Quest, pk=pk, owner=request.user)
    if quest.is_completed:
        messages.warning(request, "This quest is already completed.")
        return redirect("quests:detail", pk=quest.pk)

    level_before = get_level_info(get_total_xp(request.user))["level"]

    # These three saves either all happen or none of them do.
    with transaction.atomic():
        quest.mark_complete()
        request.user.profile.update_streak()
        new_achievements = check_achievements(request.user)

    level_after = get_level_info(get_total_xp(request.user))["level"]

    messages.success(request, f"Quest complete! You earned {quest.xp_earned} XP.")
    if level_after > level_before:
        messages.success(request, f"Level up! You are now level {level_after}.")
    for achievement in new_achievements:
        messages.info(request, f"Achievement unlocked: {achievement.name}")
    return redirect("quests:detail", pk=quest.pk)
