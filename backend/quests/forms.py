from django import forms
from django.utils import timezone

from .models import XP_REWARDS, Quest


class QuestForm(forms.ModelForm):
    """Used for both creating and editing a quest.

    owner, status and XP are left out on purpose: the owner is set from the
    logged-in user in the view, and status/XP only change through the
    Start and Complete buttons.
    """

    class Meta:
        model = Quest
        fields = ["title", "description", "category", "difficulty", "deadline"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "deadline": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "No category"
        # e.g. "XP for completing: Easy 10, Medium 25, Hard 50, Epic 100."
        rewards = ", ".join(f"{label} {XP_REWARDS[value]}" for value, label in Quest.DIFFICULTY_CHOICES)
        self.fields["difficulty"].help_text = f"XP for completing: {rewards}."

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        # Only check when the deadline was changed, so an old quest whose
        # deadline has passed can still be edited.
        if deadline and "deadline" in self.changed_data and deadline < timezone.localdate():
            raise forms.ValidationError("The deadline cannot be in the past.")
        return deadline
