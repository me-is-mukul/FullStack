from django.db import migrations

# (name, description, metric, threshold)
DEFAULT_ACHIEVEMENTS = [
    ("First Steps", "Complete your first quest.", "quests_completed", 1),
    ("Getting Serious", "Complete 5 quests.", "quests_completed", 5),
    ("Quest Master", "Complete 25 quests.", "quests_completed", 25),
    ("Dedicated", "Complete 50 quests.", "quests_completed", 50),
    ("Rising Star", "Earn 250 XP in total.", "total_xp", 250),
    ("XP Legend", "Earn 1,000 XP in total.", "total_xp", 1000),
    ("On a Roll", "Reach a 3-day streak.", "longest_streak", 3),
    ("Week Warrior", "Reach a 7-day streak.", "longest_streak", 7),
]


def add_achievements(apps, schema_editor):
    Achievement = apps.get_model("achievements", "Achievement")
    for name, description, metric, threshold in DEFAULT_ACHIEVEMENTS:
        Achievement.objects.get_or_create(
            name=name,
            defaults={"description": description, "metric": metric, "threshold": threshold},
        )


def remove_achievements(apps, schema_editor):
    Achievement = apps.get_model("achievements", "Achievement")
    Achievement.objects.filter(name__in=[row[0] for row in DEFAULT_ACHIEVEMENTS]).delete()


class Migration(migrations.Migration):
    """Adds the starting set of achievements. Staff can add more in the admin."""

    dependencies = [("achievements", "0001_initial")]

    operations = [migrations.RunPython(add_achievements, remove_achievements)]
