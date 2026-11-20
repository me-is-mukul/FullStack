from django.db import migrations

DEFAULT_CATEGORIES = [
    ("Study", "Coursework, revision and learning."),
    ("Work", "Job, internship and professional tasks."),
    ("Health", "Sleep, food and wellbeing."),
    ("Fitness", "Exercise and sport."),
    ("Personal", "Home, family and everyday life."),
    ("Finance", "Budgeting, saving and bills."),
    ("Hobby", "Creative and leisure projects."),
]


def add_categories(apps, schema_editor):
    # Use the historical model, not a direct import (standard for data migrations).
    Category = apps.get_model("quests", "Category")
    for name, description in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=name, defaults={"description": description})


def remove_categories(apps, schema_editor):
    Category = apps.get_model("quests", "Category")
    Category.objects.filter(name__in=[name for name, _ in DEFAULT_CATEGORIES]).delete()


class Migration(migrations.Migration):
    """Adds the starting list of categories. Staff can change them later in the admin."""

    dependencies = [("quests", "0001_initial")]

    operations = [migrations.RunPython(add_categories, remove_categories)]
