# reports app

[Back to README](../../README.md) · Syllabus: Unit 6 (Reporting and Data Retrieval), Unit 5 (staff-only page)

Read-only pages that summarise data from the other apps. This app has no models of its own.

## Files

| File | What is in it |
| --- | --- |
| [`views.py`](../../backend/reports/views.py) | `get_leaderboard`, `dashboard`, `my_reports`, `export_quests_csv`, `leaderboard`, `staff_report` |
| [`urls.py`](../../backend/reports/urls.py) | 5 routes, namespace `reports` |
| [`models.py`](../../backend/reports/models.py) | Empty (only a comment) |
| `templates/reports/` | `dashboard.html`, `reports.html`, `leaderboard.html`, `staff_report.html` |
| [`static/js/charts.js`](../../backend/static/js/charts.js) | Draws the charts on the reports page |

## Dashboard (`/dashboard/`)

The page users land on after logging in:

- level, total XP and a progress bar to the next level (`get_level_info`)
- current and best streak (`profile.streak_today`, `profile.longest_streak`)
- number of quests in each status (`get_status_counts`, one `aggregate()` query)
- the next 5 open quests with a deadline, the last 5 completed quests, the latest 3 achievements

## My reports (`/reports/`)

| Section | Query |
| --- | --- |
| Total XP, quests created, quests completed | `get_total_xp`, `get_status_counts` |
| XP per day, last 30 days | Completed quests grouped by `TruncDate("completed_at")` with `Sum("xp_earned")`. Days with no XP are filled with 0 in Python |
| Quests by category | `values("category__name").annotate(total=..., completed=..., xp=...)` |
| Quests by difficulty | `values("difficulty").annotate(...)`, then put in Easy to Epic order |

The view turns the per-day and per-category results into lists of labels and numbers. The
template writes them into the page with `{{ xp_chart|json_script:"xp-chart-data" }}` and
`charts.js` reads them and draws two bar charts with Chart.js. Every number is calculated in
Python; the JavaScript only draws.

## CSV export (`/reports/export/`)

`export_quests_csv` creates an `HttpResponse` with `content_type="text/csv"` and a
`Content-Disposition: attachment` header, writes a header row and one row per quest using
Python's `csv.writer`, and the browser downloads it as `my-quests.csv`. Only the logged-in
user's quests are included.

## Leaderboard (`/leaderboard/`)

`get_leaderboard()` annotates every active user with:

- `total_xp`: `Sum("quests__xp_earned")` over completed quests
- `completed_count`: `Count("quests")` over completed quests

and orders by XP, then completed quests, then username (so ties always come out in the same
order). The page shows 20 players at a time. The rank number is `rank_offset + forloop.counter`,
so page 2 continues from 21. "Your rank" is the user's position in the full list.

## Staff report (`/staff/`)

Only for staff accounts. The view checks `request.user.is_staff` and raises `PermissionDenied`
otherwise, which shows `templates/403.html`. It shows:

- active users and how many joined in the last 7 days
- quests created, completed, completion rate and total XP given out
- quests per category across all users
- top 5 players (reuses `get_leaderboard()`) and the 5 newest accounts

There is a link from here to the Django admin site.
