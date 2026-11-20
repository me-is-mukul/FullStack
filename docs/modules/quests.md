# quests app

[Back to README](../../README.md) · Syllabus: Unit 3 (ORM), Unit 4 (CRUD and Forms), Unit 6 (search and filters)

The main app of the project. Users create quests, work on them and complete them for XP.

## Files

| File | What is in it |
| --- | --- |
| [`models.py`](../../backend/quests/models.py) | `XP_REWARDS`, `Category`, `Quest` |
| [`forms.py`](../../backend/quests/forms.py) | `QuestForm` |
| [`views.py`](../../backend/quests/views.py) | `quest_list`, `quest_detail`, `quest_create`, `quest_update`, `quest_delete`, `quest_start`, `quest_complete` |
| [`utils.py`](../../backend/quests/utils.py) | `get_total_xp`, `get_level_info`, `get_status_counts` |
| [`urls.py`](../../backend/quests/urls.py) | 7 routes, namespace `quests` |
| [`admin.py`](../../backend/quests/admin.py) | `CategoryAdmin`, `QuestAdmin` |
| [`migrations/0002_default_categories.py`](../../backend/quests/migrations/0002_default_categories.py) | Adds the 7 starting categories |
| [`management/commands/seed_demo.py`](../../backend/quests/management/commands/seed_demo.py) | Demo data command |
| `templates/quests/` | `quest_list.html`, `quest_detail.html`, `quest_form.html`, `quest_confirm_delete.html` |

## Models

**Category**: `name` (unique) and `description`. One shared list for all users, managed by
staff in the admin.

**Quest**:

| Field | Notes |
| --- | --- |
| `owner` | ForeignKey to User |
| `category` | ForeignKey to Category, optional, `SET_NULL` |
| `title`, `description` | |
| `difficulty` | `easy`, `medium`, `hard` or `epic` |
| `status` | `pending`, `in_progress` or `completed` |
| `deadline` | Optional date |
| `xp_earned` | 0 until the quest is completed |
| `created_at`, `completed_at` | |

Properties: `xp_reward` (what the quest is worth), `is_completed`, `is_overdue`.
Method: `mark_complete()`.

## XP and levels

| Difficulty | XP |
| --- | --- |
| Easy | 10 |
| Medium | 25 |
| Hard | 50 |
| Epic | 100 |

These numbers are only in `XP_REWARDS` in `models.py`. The quest form builds its help text from
the same dictionary.

- Total XP = sum of `xp_earned` of the user's completed quests (`get_total_xp`).
- Level = `total_xp // 100 + 1`, so 0-99 XP is level 1, 100-199 is level 2, and so on
  (`get_level_info`).

## CRUD views

All views use `@login_required`, and every quest lookup includes `owner=request.user`:

```python
quest = get_object_or_404(Quest, pk=pk, owner=request.user)
```

So a user who types another user's quest id into the URL gets a 404.

| View | GET | POST |
| --- | --- | --- |
| `quest_create` | empty `QuestForm` | validates, `save(commit=False)`, sets `owner`, saves |
| `quest_update` | `QuestForm(instance=quest)` | validates and saves the same quest |
| `quest_delete` | confirmation page | deletes, redirects to the list |
| `quest_start` | not allowed (405) | pending to in progress |
| `quest_complete` | not allowed (405) | see below |

`QuestForm` only has `title`, `description`, `category`, `difficulty` and `deadline`. Status
and XP are not in the form, so they cannot be set by typing values into a request; they only
change through the Start and Complete buttons. `clean_deadline` stops a new deadline from being
in the past.

## Completing a quest

`quest_complete`:

1. Refuses if the quest is already completed.
2. Remembers the user's level.
3. In one `transaction.atomic()` block: `quest.mark_complete()`, then
   `profile.update_streak()`, then `check_achievements(user)`.
4. Compares the level again to show a "Level up!" message, and shows a message for each new
   achievement.

Deleting a completed quest removes its XP from the user's total as well.

## Quest list: search, filter, sort, pages

The filter bar is a GET form, so the choices appear in the URL (for example
`?q=report&status=pending&sort=deadline`). The view reads `request.GET` and builds the query
step by step:

- `q` searches title or description with `Q(title__icontains=q) | Q(description__icontains=q)`
- `status`, `category`, `difficulty` each add a `.filter()`
- `sort` picks an ordering from `SORT_OPTIONS`
- `Paginator(quests, 10)` splits the result into pages; the pagination include uses
  `{% querystring %}` so the filters stay when moving between pages
