# achievements app

[Back to README](../../README.md) · Syllabus: Unit 3 (ORM relationships), Unit 5 (Administration)

Badges that unlock automatically when a user reaches a target.

## Files

| File | What is in it |
| --- | --- |
| [`models.py`](../../backend/achievements/models.py) | `Achievement`, `UserAchievement` |
| [`utils.py`](../../backend/achievements/utils.py) | `get_user_stats`, `check_achievements` |
| [`views.py`](../../backend/achievements/views.py) | `achievement_list` |
| [`urls.py`](../../backend/achievements/urls.py) | 1 route, namespace `achievements` |
| [`admin.py`](../../backend/achievements/admin.py) | `AchievementAdmin`, `UserAchievementAdmin` |
| [`migrations/0002_default_achievements.py`](../../backend/achievements/migrations/0002_default_achievements.py) | Adds the 8 starting achievements |
| `templates/achievements/` | `achievement_list.html` |

## Models

**Achievement**: `name`, `description`, `metric` and `threshold`. The metric is one of:

| Metric | Meaning |
| --- | --- |
| `quests_completed` | Number of completed quests |
| `total_xp` | Total XP |
| `longest_streak` | Best streak in days |

An achievement unlocks when the user's value for its metric is at least the threshold.

**UserAchievement**: one row per unlock, with `user`, `achievement` and `unlocked_at`. This is
a many-to-many relationship between users and achievements, written as a separate model so it
can store the date. A `UniqueConstraint` on `(user, achievement)` means a badge can only be
unlocked once.

## Starting achievements

| Name | Unlocks at |
| --- | --- |
| First Steps | 1 quest completed |
| Getting Serious | 5 quests completed |
| Quest Master | 25 quests completed |
| Dedicated | 50 quests completed |
| Rising Star | 250 XP |
| XP Legend | 1,000 XP |
| On a Roll | 3-day streak |
| Week Warrior | 7-day streak |

Staff can add more from the admin site (Achievements > Add). The threshold must be at least 1.

## How unlocking works

`check_achievements(user)`:

1. `get_user_stats(user)` returns the three numbers as a dictionary, with the same keys as the
   metric choices.
2. It loads every achievement the user has not unlocked yet
   (`Achievement.objects.exclude(id__in=already_unlocked)`).
3. For each one whose target is reached it creates a `UserAchievement`.
4. It returns the new ones so the view can show "Achievement unlocked" messages.

It is called when a quest is completed, and again when the achievements page is opened, so an
achievement that staff add later is picked up for users who already qualify.

## Achievements page

Lists every achievement. Unlocked ones show the date; locked ones show the current value, the
target and a progress bar.
