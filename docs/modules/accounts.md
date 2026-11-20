# accounts app

[Back to README](../../README.md) · Syllabus: Unit 5 (Authentication), Unit 4 (Forms)

Handles signing up, logging in and out, the user's profile and their daily streak.

## Files

| File | What is in it |
| --- | --- |
| [`models.py`](../../backend/accounts/models.py) | `Profile` model |
| [`signals.py`](../../backend/accounts/signals.py) | `create_profile`: makes a Profile for every new User |
| [`apps.py`](../../backend/accounts/apps.py) | `ready()` imports `signals.py` so the signal is connected |
| [`forms.py`](../../backend/accounts/forms.py) | `RegisterForm`, `UserUpdateForm`, `ProfileForm` |
| [`views.py`](../../backend/accounts/views.py) | `register`, `profile` |
| [`urls.py`](../../backend/accounts/urls.py) | Our two views plus Django's login, logout and password-change views |
| [`admin.py`](../../backend/accounts/admin.py) | `ProfileAdmin` |
| `templates/accounts/` | `login.html`, `register.html`, `profile.html`, `password_change.html`, `password_change_done.html` |

## Profile model

Django's `User` already has username, email, first/last name and password. `Profile` is linked
to it with a `OneToOneField` and adds:

- `display_name`, `bio`
- `current_streak`, `longest_streak`, `last_active_date`

`profile.name` returns the display name, or the username if it is empty.

## How the streak works

`Profile.update_streak(day)` is called every time the user completes a quest.

| Last active day | What happens |
| --- | --- |
| Never active | streak = 1 |
| Same day as `day` | nothing changes (only one count per day) |
| The day before `day` | streak + 1 |
| Earlier than that (a day was missed) | streak starts again at 1 |

`longest_streak` keeps the best value. `streak_today` is what the pages show: it returns 0 if
the user's last active day was before yesterday, because the streak is already broken even
though the stored number has not been reset yet.

## Sign up and login

- `register` uses `RegisterForm`, which extends Django's `UserCreationForm` (username, password,
  password confirmation) with a required, unique email. After saving, the view calls `login()`
  so the user does not have to log in again.
- When the user is saved, the `post_save` signal creates their Profile. This also covers users
  made with `createsuperuser` or in the admin.
- Login, logout and password change are Django's own class-based views. We only pass a
  `template_name`. Logout must be a POST, so the navbar uses a small form for it.
- `LOGIN_URL`, `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` in `settings.py` decide where
  users are sent.

## Profile page

The profile page shows two forms in one `<form>`: `UserUpdateForm` (name, email) and
`ProfileForm` (display name, bio). Both must be valid before either is saved. Username,
password and staff status cannot be changed here.
