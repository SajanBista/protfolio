from django.db import models


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200, help_text="e.g. Master of Science")
    field_of_study = models.CharField(max_length=200, blank=True, help_text="e.g. Computer Science")
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if in progress.")
    is_ongoing = models.BooleanField(default=False)
    description = models.TextField(blank=True, help_text="Coursework, thesis, honors, GPA, etc.")
    logo = models.ImageField(upload_to="education/logos/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.degree} — {self.institution}"
