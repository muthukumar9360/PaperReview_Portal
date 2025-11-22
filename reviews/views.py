from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LogoutView
from django.utils import timezone
from django.urls import reverse_lazy

from .decorators import role_required
from .forms import (
    SignupForm, PaperUploadForm, AssignReviewersForm,
    ReviewForm, FinalDecisionForm
)
from .models import Paper, Review, PaperStatusHistory, Track, User


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    # Route users to their dashboards
    if request.user.role == "author":
        return redirect("author_my_papers")
    if request.user.role == "reviewer":
        return redirect("reviewer_dashboard")
    if request.user.role == "editor":
        return redirect("editor_dashboard")
    return redirect("login")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created.")
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


# ---------- Author ----------
@role_required("author")
def author_upload(request):
    if request.method == "POST":
        form = PaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.author = request.user
            paper.save()
            PaperStatusHistory.objects.create(
                paper=paper, status=paper.status, changed_by=request.user
            )
            messages.success(request, "Paper submitted successfully.")
            return redirect("author_my_papers")
    else:
        form = PaperUploadForm()
    return render(request, "reviews/author_upload.html", {"form": form})


@role_required("author")
def author_my_papers(request):
    papers = Paper.objects.filter(author=request.user).order_by("-submitted_on")
    return render(request, "reviews/author_my_papers.html", {"papers": papers})


# ---------- Editor ----------
@role_required("editor")
def editor_dashboard(request):
    context = {
        "submitted": Paper.objects.filter(status="submitted").select_related("track", "author"),
        "under_review": Paper.objects.filter(status="under_review").select_related("track", "author"),
        "decided": Paper.objects.filter(status__in=["accepted", "rejected"]).select_related("track", "author"),
    }
    return render(request, "reviews/editor_dashboard.html", context)


@role_required("editor")
def assign_reviewers(request, paper_id: int):
    paper = get_object_or_404(Paper, id=paper_id)
    if request.method == "POST":
        form = AssignReviewersForm(request.POST)
        if form.is_valid():
            selected = form.cleaned_data["reviewers"]
            created_any = False
            for r in selected:
                obj, created = Review.objects.get_or_create(paper=paper, reviewer=r)
                created_any |= created
            if created_any:
                paper.status = "under_review"
                paper.save(update_fields=["status"])
                PaperStatusHistory.objects.create(
                    paper=paper, status="under_review", changed_by=request.user
                )
            messages.success(request, "Reviewers assigned.")
            return redirect("editor_dashboard")
    else:
        form = AssignReviewersForm()
    already = set(paper.reviews.values_list("reviewer_id", flat=True))
    return render(request, "reviews/assign_reviewers.html",
                  {"paper": paper, "form": form, "already": already})


@role_required("editor")
def paper_detail(request, paper_id: int):
    paper = get_object_or_404(Paper.objects.select_related("author", "track"), id=paper_id)
    reviews = paper.reviews.select_related("reviewer")
    decision_form = FinalDecisionForm(request.POST or None)
    if request.method == "POST" and decision_form.is_valid():
        final_status = decision_form.cleaned_data["final_decision"]
        paper.status = final_status
        paper.save(update_fields=["status"])
        PaperStatusHistory.objects.create(
            paper=paper, status=final_status, changed_by=request.user
        )
        messages.success(request, f"Paper marked as {final_status}.")
        return redirect("editor_dashboard")
    return render(request, "reviews/paper_detail.html",
                  {"paper": paper, "reviews": reviews, "decision_form": decision_form})


# ---------- Reviewer ----------
@role_required("reviewer")
def reviewer_dashboard(request):
    assignments = Review.objects.filter(reviewer=request.user).select_related("paper", "paper__track", "paper__author")
    return render(request, "reviews/reviewer_dashboard.html", {"assignments": assignments})


@role_required("reviewer")
def submit_review(request, review_id: int):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            r = form.save(commit=False)
            r.reviewed_on = timezone.now()
            r.save()
            messages.success(request, "Review submitted.")
            return redirect("reviewer_dashboard")
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_form.html", {"review": review, "form": form})

    from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')



