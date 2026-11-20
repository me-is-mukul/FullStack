# Database design

[Back to README](../README.md)

The database is SQLite (`backend/db.sqlite3`). All tables are created from the models by
`python manage.py migrate`. `User` is Django's built-in user model from `django.contrib.auth`.

## ER diagram

```mermaid
erDiagram
    USER ||--|| PROFILE : has
    USER ||--o{ QUEST : owns
    CATEGORY |o--o{ QUEST : groups
    USER ||--o{ USER_ACHIEVEMENT : unlocks
    ACHIEVEMENT ||--o{ USER_ACHIEVEMENT : "unlocked as"

    USER {
        int id PK
        string username
        string email
        string password "hashed by Django"
        bool is_staff
    }
    PROFILE {
        int id PK
        int user_id FK "one-to-one"
        string display_name
        text bio
        int current_streak
        int longest_streak
        date last_active_date
    }
    CATEGORY {
        int id PK
        string name "unique"
        string description
    }
    QUEST {
        int id PK
        int owner_id FK
        int category_id FK "nullable"
        string title
        text description
        string difficulty "easy / medium / hard / epic"
        string status "pending / in_progress / completed"
        date deadline "nullable"
        int xp_earned
        datetime created_at
        datetime completed_at "nullable"
    }
    ACHIEVEMENT {
        int id PK
        string name "unique"
        string description
        string metric
        int threshold
    }
    USER_ACHIEVEMENT {
        int id PK
        int user_id FK
        int achievement_id FK
        datetime unlocked_at
    }
```

## Tables

| App | Model | Table | Purpose |
| --- | --- | --- | --- |
| Django | `User` | `auth_user` | Login details |
| accounts | `Profile` | `accounts_profile` | Display name, bio and streak |
| quests | `Category` | `quests_category` | Shared list of categories |
| quests | `Quest` | `quests_quest` | Each user's quests |
| achievements | `Achievement` | `achievements_achievement` | The list of badges |
| achievements | `UserAchievement` | `achievements_userachievement` | Which user unlocked which badge, and when |

## Relationships

| Relationship | Field | Type | `on_delete` | Why |
| --- | --- | --- | --- | --- |
| User - Profile | `Profile.user` | One-to-one | `CASCADE` | Deleting a user deletes their profile |
| User - Quest | `Quest.owner` | Many-to-one (ForeignKey) | `CASCADE` | Deleting a user deletes their quests |
| Category - Quest | `Quest.category` | Many-to-one, optional | `SET_NULL` | Deleting a category keeps its quests, just without a category |
| User - Achievement | `UserAchievement` | Many-to-many through a model | `CASCADE` on both sides | The extra table stores `unlocked_at` |

The `related_name` on each foreign key lets us go backwards, for example `user.quests.all()`,
`user.profile` and `user.achievements.all()`.

## Rules kept by the database

- `Category.name` and `Achievement.name` are unique.
- `UserAchievement` has a `UniqueConstraint` on `(user, achievement)`, so a badge can only be
  unlocked once per user.
- `Profile.user` is one-to-one, so each user has exactly one profile.

## Values that are calculated, not stored

| Value | How it is worked out |
| --- | --- |
| Total XP | `Sum("xp_earned")` over the user's completed quests (`quests/utils.py`) |
| Level | `total_xp // 100 + 1` |
| Leaderboard rank | Position in a query ordered by total XP, completed count, username |
| Streak shown today | `Profile.streak_today` returns 0 if the last active day was before yesterday |

`xp_earned` is saved on the quest when it is completed, so if the difficulty is changed later
the XP already earned stays the same.

## Data migrations

Two migrations add starting data, so a fresh database is ready to use:

- `quests/migrations/0002_default_categories.py` adds Study, Work, Health, Fitness, Personal,
  Finance and Hobby.
- `achievements/migrations/0002_default_achievements.py` adds the 8 achievements.

## Some ORM queries used in the project

```python
# Filter + search (quests/views.py)
Quest.objects.filter(owner=request.user).filter(
    Q(title__icontains=query) | Q(description__icontains=query)
)

# Several counts in one query (quests/utils.py)
Quest.objects.filter(owner=user).aggregate(
    total=Count("id"),
    completed=Count("id", filter=Q(status="completed")),
)

# GROUP BY category (reports/views.py)
my_quests.values("category__name").annotate(total=Count("id"), xp=Sum("xp_earned"))

# XP per day: GROUP BY the date part of completed_at (reports/views.py)
my_quests.filter(status="completed").annotate(day=TruncDate("completed_at")) \
    .values("day").annotate(xp=Sum("xp_earned"))

# Leaderboard: annotate every user with totals from their quests (reports/views.py)
User.objects.annotate(
    total_xp=Sum("quests__xp_earned", filter=Q(quests__status="completed"), default=0),
    completed_count=Count("quests", filter=Q(quests__status="completed")),
).order_by("-total_xp", "-completed_count", "username")
```
