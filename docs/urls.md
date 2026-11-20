# URL map

[Back to README](../README.md)

**Access:** Public = anyone. User = must be logged in. Owner = logged in and the quest is
theirs (anyone else gets a 404). Staff = an account with `is_staff` (anyone else gets a 403).

Pages that change data only accept POST and include a CSRF token. After a successful POST the
view redirects to another page and shows a message.

## Main site (`questforge/urls.py`)

| URL | Name | Access | Page |
| --- | --- | --- | --- |
| `/` | `home` | Public | Landing page. Logged-in users are sent to the dashboard |
| `/admin/` | `admin:index` | Staff | Django admin site |

## Accounts (`accounts/urls.py`)

| URL | Name | Method | Access | Page |
| --- | --- | --- | --- | --- |
| `/accounts/register/` | `register` | GET, POST | Public | Sign-up form |
| `/accounts/login/` | `login` | GET, POST | Public | Django's `LoginView` |
| `/accounts/logout/` | `logout` | POST | User | Django's `LogoutView` |
| `/accounts/profile/` | `profile` | GET, POST | User | View and edit own profile |
| `/accounts/password/` | `password_change` | GET, POST | User | Django's `PasswordChangeView` |
| `/accounts/password/done/` | `password_change_done` | GET | User | Confirmation |

## Quests (`quests/urls.py`, namespace `quests`)

| URL | Name | Method | Access | Page |
| --- | --- | --- | --- | --- |
| `/quests/` | `quests:list` | GET | User | Own quests with search, filters, sorting, pages |
| `/quests/new/` | `quests:create` | GET, POST | User | Create form |
| `/quests/<id>/` | `quests:detail` | GET | Owner | Quest details and action buttons |
| `/quests/<id>/edit/` | `quests:update` | GET, POST | Owner | Edit form |
| `/quests/<id>/delete/` | `quests:delete` | GET, POST | Owner | Confirm, then delete |
| `/quests/<id>/start/` | `quests:start` | POST | Owner | Pending to in progress |
| `/quests/<id>/complete/` | `quests:complete` | POST | Owner | Complete, give XP, update streak and achievements |

Query parameters for the list: `q` (search), `status`, `category` (id), `difficulty`, `sort`
(`newest`, `oldest`, `deadline`, `title`) and `page`. Example:
`/quests/?status=pending&sort=deadline`.

## Achievements (`achievements/urls.py`, namespace `achievements`)

| URL | Name | Access | Page |
| --- | --- | --- | --- |
| `/achievements/` | `achievements:list` | User | All achievements with progress |

## Reports (`reports/urls.py`, namespace `reports`)

| URL | Name | Access | Page |
| --- | --- | --- | --- |
| `/dashboard/` | `reports:dashboard` | User | Level, streak, counts, deadlines, recent activity |
| `/reports/` | `reports:reports` | User | Charts and tables of own data |
| `/reports/export/` | `reports:export` | User | Downloads own quests as `my-quests.csv` |
| `/leaderboard/` | `reports:leaderboard` | User | All users ranked by XP |
| `/staff/` | `reports:staff` | Staff | Totals for the whole site |
