import markdown as md
from django.db import models


class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200, help_text="e.g. Data Engineer")
    location = models.CharField(max_length=120, blank=True)
    employment_type = models.CharField(
        max_length=60, blank=True, help_text="e.g. Full-time, Contract, Internship"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if this is your current role.")
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, help_text="Responsibilities & impact. Markdown supported.")
    company_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="experience/logos/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"

    def description_html(self):
        return md.markdown(self.description, extensions=["fenced_code", "tables"])
