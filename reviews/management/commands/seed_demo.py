from django.core.management.base import BaseCommand
from reviews.models import User, Track

class Command(BaseCommand):
    help = "Create demo users and tracks"

    def handle(self, *args, **options):
        # Tracks
        for name in ["Artificial Intelligence", "Networks", "Databases"]:
            Track.objects.get_or_create(name=name)

        # Users with known passwords
        users = [
            ("author1", "author1@example.com", "author"),
            ("author2", "author2@example.com", "author"),
            ("reviewer1", "reviewer1@example.com", "reviewer"),
            ("reviewer2", "reviewer2@example.com", "reviewer"),
            ("editor1", "editor1@example.com", "editor"),
        ]
        for u, e, r in users:
            obj, created = User.objects.get_or_create(username=u, defaults={"email": e, "role": r})
            if created:
                obj.set_password("pass1234")
                obj.save()

        self.stdout.write(self.style.SUCCESS("Seeded demo users (pass: pass1234) and tracks."))
