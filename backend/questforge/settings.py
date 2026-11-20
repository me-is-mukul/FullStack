"""
Django settings for the QuestForge project.

For the full list of settings see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""
import os
from pathlib import Path

from django.contrib.messages import constants as message_constants

# backend/ folder (the one that holds manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# The fallback key is only for running the project locally.
# On a real server, set the DJANGO_SECRET_KEY environment variable.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-questforge-local-development-key"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Applications

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Our apps
    "accounts",
    "quests",
    "achievements",
    "reports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "questforge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # base.html and the shared includes live in backend/templates/.
        # Each app also has its own templates/<app_name>/ folder.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "questforge.wsgi.application"


# Database (SQLite file inside backend/)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Where @login_required sends people, and where login/logout take them.
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "reports:dashboard"
LOGOUT_REDIRECT_URL = "home"


# Internationalisation

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, images)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# Bootstrap calls its red alert "danger", Django calls it "error".
MESSAGE_TAGS = {message_constants.ERROR: "danger"}
