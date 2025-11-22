from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),

    # Author
    path("author/upload/", views.author_upload, name="author_upload"),
    path("author/my-papers/", views.author_my_papers, name="author_my_papers"),

    # Editor
    path("editor/", views.editor_dashboard, name="editor_dashboard"),
    path("editor/paper/<int:paper_id>/assign/", views.assign_reviewers, name="assign_reviewers"),
    path("editor/paper/<int:paper_id>/", views.paper_detail, name="paper_detail"),

    # Reviewer
    path("reviewer/", views.reviewer_dashboard, name="reviewer_dashboard"),
    path("review/<int:review_id>/submit/", views.submit_review, name="submit_review"),

    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
