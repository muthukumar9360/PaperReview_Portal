from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ("author", "Author"),
        ("reviewer", "Reviewer"),
        ("editor", "Editor"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"


class Track(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Paper(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    title = models.CharField(max_length=200)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    file_link = models.FileField(upload_to="papers/")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="papers",
                               limit_choices_to={"role": "author"})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} [{self.get_status_display()}]"


class Review(models.Model):
    DECISION_CHOICES = [("accept", "Accept"), ("reject", "Reject")]

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_reviews",
        limit_choices_to={"role": "reviewer"}
    )
    comments = models.TextField(blank=True)
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES, blank=True)
    reviewed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("paper", "reviewer")

    def __str__(self) -> str:
        return f"Review({self.paper_id} by {self.reviewer.username})"


class PaperStatusHistory(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=20, choices=Paper.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.paper_id}: {self.status} @ {self.changed_on:%Y-%m-%d %H:%M}"
