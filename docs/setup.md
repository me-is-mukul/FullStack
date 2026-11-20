# Setup guide

[Back to README](../README.md)

## What you need

- Python 3.10 or newer (we used 3.13)
- Nothing else. SQLite comes with Python, and Bootstrap and Chart.js are already in
  `backend/static/vendor/`, so the site also works without internet.

## First-time setup

Run these from the project folder (the one with `README.md` in it).

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then, on any system:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## What each command does

| Command (run inside `backend/`) | What it does |
| --- | --- |
| `python manage.py migrate` | Creates all tables in `db.sqlite3`. It also adds the 7 default categories and the 8 default achievements (these are data migrations) |
| `python manage.py createsuperuser` | Creates an admin account. It can open `/admin/` and the staff report at `/staff/` |
| `python manage.py seed_demo` | Optional. Creates 5 demo users with completed and open quests, so the charts and leaderboard have data. Running it twice does nothing the second time |
| `python manage.py runserver` | Starts the development server on port 8000 |

## Demo accounts

After `seed_demo`: `aarav`, `diya`, `kabir`, `meera`, `rohan`, all with the password
`questforge-demo`. None of them is staff.

## Starting again with an empty database

Stop the server, delete `backend/db.sqlite3`, then run `python manage.py migrate` again (and
`createsuperuser` / `seed_demo` if you want them).

## Settings you might change

Everything is in [`backend/questforge/settings.py`](../backend/questforge/settings.py).

| Setting | Value | Note |
| --- | --- | --- |
| `TIME_ZONE` | `Asia/Kolkata` | Used for deadlines, "today" and streak days |
| `DEBUG` | `True` | Can be turned off with the environment variable `DJANGO_DEBUG=False`. With `DEBUG` off, `runserver` does not serve CSS/JS, so keep it on for local use |
| `SECRET_KEY` | a development key | On a real server, set the environment variable `DJANGO_SECRET_KEY` |
| `DATABASES` | SQLite file `backend/db.sqlite3` | |
