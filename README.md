# QuestForge

QuestForge is a goal tracker built with Django for our Full Stack Development lab.

You add your tasks as **quests**. Completing a quest gives you **XP** (experience points), every
100 XP is a new **level**, completing quests on days in a row builds a **streak**, and reaching
milestones unlocks **achievements**. Each user also gets a dashboard, a reports page with charts
and a leaderboard. Staff get a site-wide report and the Django admin.

## Features

- Sign up, log in, log out, edit profile, change password
- Create, view, edit and delete quests, each with a category, difficulty and optional deadline
- Search, filter, sort and paginate the quest list
- XP for completed quests (Easy 10, Medium 25, Hard 50, Epic 100) and levels
- Daily streak and 8 achievements (staff can add more from the admin)
- Dashboard, reports page with charts, CSV download of your quests, leaderboard
- Staff-only report and the Django admin site

## Tech used

| Part | Technology |
| --- | --- |
| Language | Python 3.13 |
| Framework | Django 5.2 |
| Database | SQLite, through the Django ORM |
| Frontend | Django templates, Bootstrap 5.3, Chart.js 4.4 (stored in `backend/static/vendor/`) |

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser      # an admin/staff account
python manage.py seed_demo            # optional: 5 demo users with quests
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Demo users are `aarav`, `diya`, `kabir`, `meera` and `rohan`, all
with the password `questforge-demo`. More detail is in the [setup guide](docs/setup.md).

## Documentation

| Document | What it covers |
| --- | --- |
| [Syllabus mapping](docs/syllabus-mapping.md) | Which part of the project covers each unit of the syllabus |
| [Architecture](docs/architecture.md) | Folder structure, the four apps, how a request is handled |
| [Database design](docs/database.md) | Models, relationships, ER diagram, important queries |
| [URL map](docs/urls.md) | Every page, its URL name and who can open it |
| [Setup guide](docs/setup.md) | Installing, running, demo data, resetting the database |

Notes on each app:
[accounts](docs/modules/accounts.md) ·
[quests](docs/modules/quests.md) ·
[achievements](docs/modules/achievements.md) ·
[reports](docs/modules/reports.md)

## Project structure

```text
project/
├── README.md
├── requirements.txt
├── docs/                  documentation (linked above)
└── backend/
    ├── manage.py
    ├── questforge/        project settings and main urls.py
    ├── accounts/          sign up, login, profile, streak
    ├── quests/            categories and quests (CRUD), XP
    ├── achievements/      achievements and unlocking them
    ├── reports/           dashboard, reports, leaderboard, staff report
    ├── templates/         base.html, home page, error pages, shared includes
    └── static/            css, js, Bootstrap and Chart.js
```
