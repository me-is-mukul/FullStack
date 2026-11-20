"""ASGI config for the QuestForge project."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questforge.settings")

application = get_asgi_application()
