from django.contrib import admin
from .models import User, Track, Paper, Review, PaperStatusHistory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")
    search_fields = ("username", "email")

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "track", "author", "status", "submitted_on")
    list_filter = ("status", "track")
    search_fields = ("title", "author__username")
    inlines = [ReviewInline]

@admin.register(PaperStatusHistory)
class PaperStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("paper", "status", "changed_by", "changed_on")
    list_filter = ("status",)
