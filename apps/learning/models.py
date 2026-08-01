import markdown as md
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class LearningLog(models.Model):
    """
    A single day's learning activity.

    Each entry gets an auto-incrementing ticket number (LEARN-0001, LEARN-0002, ...)
    which doubles as the suggested Git branch name / GitHub issue title prefix,
    so daily learning can be tracked as a real GitHub issue + branch.
    """

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    ticket_number = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.CharField(max_length=300, blank=True, help_text="One-line summary for the list page.")
    notes = models.TextField(blank=True, help_text="What you learned today. Markdown supported.")
    topic = models.CharField(max_length=120, blank=True, help_text="e.g. AWS, Django, Web Scraping, SQL")
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

    # GitHub linkage
    github_issue_number = models.PositiveIntegerField(null=True, blank=True)
    github_issue_url = models.URLField(blank=True)
    branch_name = models.CharField(max_length=200, blank=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"[{self.ticket_number}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self._next_ticket_number()
        if not self.slug:
            self.slug = slugify(f"{self.ticket_number}-{self.title}")
        if not self.branch_name:
            self.branch_name = f"learn/{self.ticket_number.lower()}-{slugify(self.title)}"
        super().save(*args, **kwargs)

    @staticmethod
    def _next_ticket_number():
        last = LearningLog.objects.order_by("-id").first()
        next_id = (last.id + 1) if last else 1
        return f"LEARN-{next_id:04d}"

    def get_absolute_url(self):
        return reverse("learning:detail", kwargs={"slug": self.slug})

    def notes_html(self):
        return md.markdown(self.notes, extensions=["fenced_code", "codehilite", "tables"])
