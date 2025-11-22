from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import User, Track, Paper, Review, PaperStatusHistory

class FlowTest(TestCase):
    def setUp(self):
        self.track = Track.objects.create(name="AI")
        self.author = User.objects.create_user(username="a1", password="p", role="author")
        self.reviewer = User.objects.create_user(username="r1", password="p", role="reviewer")
        self.editor = User.objects.create_user(username="e1", password="p", role="editor")

    def test_full_flow(self):
        # Author submits a paper
        self.client.login(username="a1", password="p")
        pdf = SimpleUploadedFile("p.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        resp = self.client.post(reverse("author_upload"), {
            "title": "My Paper",
            "track": self.track.id,
        }, follow=True)
        # Missing file should render form (bad request)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse("author_upload"), {
            "title": "My Paper",
            "track": self.track.id,
            "file_link": pdf
        }, follow=True)
        self.assertContains(resp, "Paper submitted successfully.")
        paper = Paper.objects.get(title="My Paper")
        self.assertEqual(paper.status, "submitted")
        self.assertTrue(PaperStatusHistory.objects.filter(paper=paper, status="submitted").exists())
        self.client.logout()

        # Editor assigns reviewer
        self.client.login(username="e1", password="p")
        resp = self.client.post(reverse("assign_reviewers", args=[paper.id]), {
            "reviewers": [self.reviewer.id]
        }, follow=True)
        self.assertContains(resp, "Reviewers assigned.")
        paper.refresh_from_db()
        self.assertEqual(paper.status, "under_review")
        self.assertTrue(Review.objects.filter(paper=paper, reviewer=self.reviewer).exists())
        self.client.logout()

        # Reviewer submits review
        self.client.login(username="r1", password="p")
        review = Review.objects.get(paper=paper, reviewer=self.reviewer)
        resp = self.client.post(reverse("submit_review", args=[review.id]), {
            "comments": "Looks good",
            "decision": "accept"
        }, follow=True)
        self.assertContains(resp, "Review submitted.")
        review.refresh_from_db()
        self.assertEqual(review.decision, "accept")
        self.client.logout()

        # Editor makes final decision
        self.client.login(username="e1", password="p")
        resp = self.client.post(reverse("paper_detail", args=[paper.id]), {
            "final_decision": "accepted"
        }, follow=True)
        self.assertContains(resp, "Paper marked as accepted.")
        paper.refresh_from_db()
        self.assertEqual(paper.status, "accepted")
        self.assertTrue(PaperStatusHistory.objects.filter(paper=paper, status="accepted").exists())
