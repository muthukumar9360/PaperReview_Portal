from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Paper, Review

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "email", "role",)

class PaperUploadForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ("title", "track", "file_link")

class AssignReviewersForm(forms.Form):
    reviewers = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reviewers"].queryset = User.objects.filter(role="reviewer")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("comments", "decision")
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 6}),
        }

class FinalDecisionForm(forms.Form):
    DECISION = (
        ("accepted", "Accept"),
        ("rejected", "Reject"),
    )
    final_decision = forms.ChoiceField(choices=DECISION)
