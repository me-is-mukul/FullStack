# Architecture

[Back to README](../README.md)

QuestForge is one Django **project** (`questforge`) made of four **apps**. Each app looks after
one part of the site and has the usual Django files: `models.py`, `views.py`, `urls.py`,
`forms.py`, `admin.py` and a `templates/<app>/` folder.

## Folder structure

```text
backend/
├── manage.py                     command-line tool (runserver, migrate, ...)
├── questforge/                   the project package
│   ├── settings.py               installed apps, database, templates, static files, login URLs
│   ├── urls.py                   main URL list, includes each app's urls.py
│   ├── views.py                  the home (landing) page
│   └── wsgi.py / asgi.py         entry points for a web server
├── accounts/                     users and profiles
│   ├── models.py                 Profile (display name, bio, streak)
│   ├── signals.py                creates a Profile whenever a User is created
│   ├── forms.py                  RegisterForm, UserUpdateForm, ProfileForm
│   ├── views.py                  register, profile
│   ├── urls.py                   also wires Django's built-in login/logout/password views
│   ├── admin.py
│   └── templates/accounts/
├── quests/                       the main CRUD app
│   ├── models.py                 Category, Quest, XP_REWARDS
│   ├── forms.py                  QuestForm (ModelForm)
│   ├── views.py                  list, detail, create, update, delete, start, complete
│   ├── utils.py                  total XP, level, status counts
│   ├── urls.py, admin.py
│   ├── migrations/0002_default_categories.py
│   ├── management/commands/seed_demo.py
│   └── templates/quests/
├── achievements/
│   ├── models.py                 Achievement, UserAchievement
│   ├── utils.py                  get_user_stats, check_achievements
│   ├── views.py, urls.py, admin.py
│   ├── migrations/0002_default_achievements.py
│   └── templates/achievements/
├── reports/                      read-only pages, no tables of its own
│   ├── views.py                  dashboard, my_reports, export_quests_csv, leaderboard, staff_report
│   ├── urls.py
│   └── templates/reports/
├── templates/                    shared templates
│   ├── base.html                 the layout every page extends
│   ├── home.html, 403.html, 404.html
│   └── includes/                 navbar, messages, form_fields, pagination, quest_badges
└── static/
    ├── css/style.css             our colours and a few classes on top of Bootstrap
    ├── js/charts.js              draws the two charts on the reports page
    ├── img/logo.svg              favicon
    └── vendor/                   Bootstrap 5.3 and Chart.js 4.4 (downloaded copies)
```

## How the apps use each other

```text
accounts      (no imports from our other apps)
quests        -> achievements.utils.check_achievements   (after a quest is completed)
achievements  -> quests.models, quests.utils             (to count quests and XP)
reports       -> quests.models, quests.utils             (to build the reports)
```

`reports` has no models. It only reads the tables of the other apps.

## What happens on a request

Example: the user clicks **Mark as complete** on quest 42.

1. The browser sends `POST /quests/42/complete/` with the CSRF token.
2. `questforge/urls.py` sends anything starting with `quests/` to `quests/urls.py`, which maps
   `<int:pk>/complete/` to `views.quest_complete` with `pk=42`.
3. `@login_required` checks the user is logged in. `@require_POST` refuses a GET request.
4. `get_object_or_404(Quest, pk=42, owner=request.user)` loads the quest. If it belongs to
   someone else, the user gets a 404.
5. Inside `transaction.atomic()` the view:
   - calls `quest.mark_complete()`, which sets the status, the completion time and `xp_earned`
   - calls `request.user.profile.update_streak()`
   - calls `check_achievements(request.user)`, which unlocks any achievement now reached
6. It adds success messages ("You earned 50 XP", "Level up!", "Achievement unlocked") and
   redirects to the quest page (POST, then redirect, then GET).
7. The quest page template extends `base.html`, which shows the messages at the top.

## Templates

Every page template starts with `{% extends "base.html" %}` and fills in the `title` and
`content` blocks. The reports page also fills the `scripts` block to load Chart.js.

```text
base.html
├── includes/navbar.html      (included)
├── includes/messages.html    (included)
└── {% block content %}       filled by each page, e.g. quests/quest_list.html
                               which itself includes includes/pagination.html
```

Django finds app templates through `APP_DIRS = True` and the shared ones through
`DIRS = [BASE_DIR / "templates"]` in `settings.py`.

## Static files

`base.html` loads `vendor/bootstrap/bootstrap.min.css`, then `css/style.css`, and
`vendor/bootstrap/bootstrap.bundle.min.js` (for the mobile menu, dropdown and closable alerts).
JavaScript is only used for these and for drawing charts. All rules (XP, streaks, permissions)
are in Python.
