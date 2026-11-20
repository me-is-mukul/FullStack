"""Creates demo users and quests so the dashboard and reports have data to show.

Usage:  python manage.py seed_demo
"""
import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from achievements.utils import check_achievements
from quests.models import Category, Quest

DEMO_USERS = ["aarav", "diya", "kabir", "meera", "rohan"]
DEMO_PASSWORD = "questforge-demo"
DIFFICULTIES = ["easy", "easy", "medium", "medium", "hard", "epic"]

# (title, category name)
QUEST_IDEAS = [
    ("Finish the DBMS assignment", "Study"),
    ("Revise for the quiz", "Study"),
    ("Read two chapters", "Study"),
    ("Solve five coding problems", "Study"),
    ("Prepare the presentation", "Work"),
    ("Update my resume", "Work"),
    ("Morning run", "Fitness"),
    ("Gym session", "Fitness"),
    ("Meditate for ten minutes", "Health"),
    ("Sleep by eleven", "Health"),
    ("Clean the desk", "Personal"),
    ("Plan the week", "Personal"),
    ("Track monthly spending", "Finance"),
    ("Sketch for an hour", "Hobby"),
]


class Command(BaseCommand):
    help = "Create five demo users with some completed and some open quests."

    def handle(self, *args, **options):
        if User.objects.filter(username__in=DEMO_USERS).exists():
            self.stdout.write("Demo users already exist. Nothing was changed.")
            return

        rng = random.Random(42)  # fixed seed, so the data is the same every time
        categories = {category.name: category for category in Category.objects.all()}
        now = timezone.now()

        for index, username in enumerate(DEMO_USERS):
            user = User.objects.create_user(username, f"{username}@example.com", DEMO_PASSWORD)

            # Completed quests on some of the last 14 days, oldest first,
            # so the streak is built up in the right order.
            days_ago = sorted(rng.sample(range(14), 5 + index), reverse=True)
            for days in days_ago:
                title, category_name = rng.choice(QUEST_IDEAS)
                quest = Quest.objects.create(
                    owner=user,
                    title=title,
                    category=categories.get(category_name),
                    difficulty=rng.choice(DIFFICULTIES),
                )
                completed_at = now - timedelta(days=days)
                quest.mark_complete(when=completed_at)
                user.profile.update_streak(timezone.localdate(completed_at))
            check_achievements(user)

            # A few open quests with upcoming deadlines.
            for offset in range(3):
                title, category_name = rng.choice(QUEST_IDEAS)
                Quest.objects.create(
                    owner=user,
                    title=title,
                    category=categories.get(category_name),
                    difficulty=rng.choice(DIFFICULTIES),
                    deadline=timezone.localdate() + timedelta(days=offset + 1 + index),
                )

        self.stdout.write(self.style.SUCCESS(
            f"Created demo users {', '.join(DEMO_USERS)} (password: {DEMO_PASSWORD})."
        ))
