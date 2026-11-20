# Syllabus mapping

[Back to README](../README.md)

This table shows where each unit of the Full Stack Development syllabus is used in QuestForge.
File paths are inside `backend/`.

| # | Unit | Main places in the project |
| --- | --- | --- |
| 1 | Python and Django Fundamentals | `questforge/` project, `manage.py`, `settings.py`, the four apps, `seed_demo` command |
| 2 | Website Development and Template Inheritance | `templates/base.html`, `templates/includes/`, every app's `templates/` folder, `static/` |
| 3 | Database Applications using Django ORM | All `models.py` files, migrations, `quests/utils.py`, `achievements/utils.py` |
| 4 | CRUD Operations and Forms | `quests/` (create, read, update, delete), `quests/forms.py`, `accounts/forms.py` |
| 5 | Authentication and Administration | `accounts/`, `@login_required`, staff check, every `admin.py` |
| 6 | Reporting and Data Retrieval | `reports/` (dashboard, reports, CSV, leaderboard, staff report), quest search and filters |

## 1. Python and Django Fundamentals

| Topic | Where |
| --- | --- |
| Project vs apps | One project ([`questforge/`](../backend/questforge/)) and four apps registered in `INSTALLED_APPS` in [`settings.py`](../backend/questforge/settings.py) |
| `manage.py` commands | `runserver`, `makemigrations`, `migrate`, `createsuperuser`, plus our own `seed_demo` ([`quests/management/commands/seed_demo.py`](../backend/quests/management/commands/seed_demo.py)) |
| Settings | Database, templates, static files, time zone and login URLs in [`settings.py`](../backend/questforge/settings.py) |
| URL routing | [`questforge/urls.py`](../backend/questforge/urls.py) uses `include()` for each app's `urls.py`; apps use `app_name` namespaces and path converters like `<int:pk>` |
| Function-based views | All our views are plain functions that take `request` and return `render()` or `redirect()` |
| Python basics | Dictionaries (`XP_REWARDS`, `SORT_OPTIONS`), list comprehensions (chart data), f-strings (messages), classes and properties (models), `datetime`/`timedelta` (streaks, 30-day chart), the `csv` module (export) |

## 2. Website Development and Template Inheritance

| Topic | Where |
| --- | --- |
| Base template | [`templates/base.html`](../backend/templates/base.html) defines the layout and the `title`, `content` and `scripts` blocks |
| `{% extends %}` | Every page starts with `{% extends "base.html" %}` |
| `{% include %}` | Navbar, messages, form fields, pagination and quest badges in [`templates/includes/`](../backend/templates/includes/) |
| Template tags and filters | `{% for %}`/`{% empty %}`, `{% if %}`, `{% url %}`, `{% csrf_token %}`, `{% static %}`, `{% querystring %}`, and filters such as `date`, `default`, `pluralize`, `linebreaksbr`, `add`, `json_script` |
| Static files | [`static/css/style.css`](../backend/static/css/style.css), [`static/js/charts.js`](../backend/static/js/charts.js), Bootstrap and Chart.js in `static/vendor/` |
| Responsive layout | Bootstrap grid (`row`, `col-md-6`, ...) and the collapsing navbar |
| Custom error pages | [`templates/403.html`](../backend/templates/403.html) and [`templates/404.html`](../backend/templates/404.html). Django uses them automatically because of their names (while `DEBUG` is on, Django shows its own debug page for 404s instead) |

## 3. Database Applications using Django ORM

| Topic | Where |
| --- | --- |
| Models and field types | `CharField`, `TextField`, `DateField`, `DateTimeField`, `PositiveIntegerField`, `ForeignKey`, `OneToOneField` in [`quests/models.py`](../backend/quests/models.py), [`accounts/models.py`](../backend/accounts/models.py), [`achievements/models.py`](../backend/achievements/models.py) |
| Choices | `Quest.DIFFICULTY_CHOICES`, `Quest.STATUS_CHOICES`, `Achievement.METRIC_CHOICES`, shown with `get_..._display()` |
| Relationships | One-to-one (User-Profile), one-to-many (User-Quest, Category-Quest), many-to-many through a model (User-Achievement via `UserAchievement`) |
| `on_delete` options | `CASCADE` and `SET_NULL`, explained in [database.md](database.md) |
| `Meta` options | `ordering`, `verbose_name_plural`, `UniqueConstraint` |
| Model methods and properties | `Quest.mark_complete()`, `Quest.is_overdue`, `Profile.update_streak()`, `Profile.streak_today` |
| Migrations | `0001_initial` in each app, and data migrations that add default categories and achievements |
| Querying | `filter`, `exclude`, `get_object_or_404`, `Q` objects for OR search, `order_by`, slicing |
| Aggregation | `aggregate()` with `Count`/`Sum` and `filter=`, `values().annotate()` for GROUP BY, `TruncDate` for per-day totals |
| Avoiding extra queries | `select_related("category")` on the quest list |
| Transactions | `transaction.atomic()` in `quest_complete` so XP, streak and achievements are saved together |
| Signals | [`accounts/signals.py`](../backend/accounts/signals.py) creates a Profile when a User is created |

## 4. CRUD Operations and Forms

The `quests` app is the full CRUD example ([`quests/views.py`](../backend/quests/views.py)):

| Operation | View | URL |
| --- | --- | --- |
| Create | `quest_create` | `/quests/new/` |
| Read (list) | `quest_list` | `/quests/` |
| Read (one) | `quest_detail` | `/quests/<id>/` |
| Update | `quest_update` | `/quests/<id>/edit/` |
| Delete | `quest_delete` (asks for confirmation first) | `/quests/<id>/delete/` |

| Topic | Where |
| --- | --- |
| `ModelForm` | `QuestForm` in [`quests/forms.py`](../backend/quests/forms.py); `UserUpdateForm`, `ProfileForm` in [`accounts/forms.py`](../backend/accounts/forms.py) |
| Extending a built-in form | `RegisterForm` extends Django's `UserCreationForm` and adds an email field |
| Validation | `clean_deadline` (no past deadlines), `clean_email` (no duplicate emails), Django's password validators |
| Widgets | `Textarea` and `DateInput(type="date")` set in `Meta.widgets` |
| `commit=False` | `quest_create` sets `quest.owner = request.user` before saving |
| Editing with `instance=` | `quest_update` and `profile` pass the existing object to the form |
| Two forms on one page | The profile page saves `UserUpdateForm` and `ProfileForm` together |
| GET form | The search/filter bar on the quest list uses `method="get"` |
| POST + CSRF + redirect | Every form that changes data uses POST, `{% csrf_token %}`, and redirects after success |
| Messages framework | `messages.success(...)` and friends, shown by `includes/messages.html` |

## 5. Authentication and Administration

| Topic | Where |
| --- | --- |
| Sign up | `register` view in [`accounts/views.py`](../backend/accounts/views.py) logs the new user in with `login()` |
| Login / logout | Django's `LoginView` and `LogoutView` in [`accounts/urls.py`](../backend/accounts/urls.py), with our own templates |
| Password change | Django's `PasswordChangeView` and `PasswordChangeDoneView` |
| Password storage | Django hashes passwords; `AUTH_PASSWORD_VALIDATORS` in settings enforce strong passwords |
| Protecting pages | `@login_required` on every page except home, login and sign-up; `LOGIN_URL` sends visitors to the login page |
| Only your own data | Every quest query uses `owner=request.user`, so other users' quests give a 404 |
| Staff-only page | `staff_report` raises `PermissionDenied` (403) unless `request.user.is_staff` |
| Templates that know the user | `{% if user.is_authenticated %}` and `{% if user.is_staff %}` in the navbar |
| Django admin | Every model is registered in its app's `admin.py` with `list_display`, `list_filter`, `search_fields` and `readonly_fields`; site titles are set in [`questforge/urls.py`](../backend/questforge/urls.py) |
| Admin as a tool | Staff add categories and new achievements from the admin without changing code |

## 6. Reporting and Data Retrieval

All in [`reports/views.py`](../backend/reports/views.py) unless noted.

| Report | What it retrieves |
| --- | --- |
| Quest list (`quests/views.py`) | Search with `icontains`, filters by status, category and difficulty, four sort orders, 10 per page with `Paginator` |
| Dashboard | Level and XP progress, streak, counts per status, next 5 deadlines, last 5 completed quests, latest achievements |
| My reports | Totals, XP per day for 30 days (bar chart), quests per category (bar chart and table), quests per difficulty (table) |
| CSV export | `export_quests_csv` returns an `HttpResponse` with `text/csv` that the browser downloads |
| Leaderboard | All users annotated with total XP and completed quests, ranked and paginated, with "your rank" |
| Staff report | Site-wide totals, completion rate, new users this week, quests per category, top 5 players, newest accounts |
| Achievements page (`achievements/views.py`) | Each achievement with the user's current value and a progress bar |

Charts: the view builds plain lists of labels and numbers, the template outputs them with the
`json_script` filter, and [`static/js/charts.js`](../backend/static/js/charts.js) draws them with
Chart.js.
