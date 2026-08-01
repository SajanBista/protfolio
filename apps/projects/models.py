import markdown as md
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.CharField(max_length=300, help_text="One-line summary shown on the projects grid.")
    description = models.TextField(blank=True, help_text="Full write-up. Markdown supported.")
    tech_stack = models.CharField(
        max_length=300, blank=True, help_text="Comma-separated, e.g. Python, Django, AWS Lambda, PostgreSQL"
    )
    cover_image = models.ImageField(upload_to="projects/covers/", blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show prominently on the home page.")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    def description_html(self):
        return md.markdown(self.description, extensions=["fenced_code", "codehilite", "tables"])
