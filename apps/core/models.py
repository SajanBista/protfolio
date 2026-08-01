from django.db import models


class Profile(models.Model):
    """Singleton-style model holding the owner's bio/about info shown on the home page."""

    full_name = models.CharField(max_length=120, default="Sajan Bista")
    headline = models.CharField(
        max_length=200,
        default="Data Engineer",
        help_text="Short professional title, e.g. 'Data Engineer | AWS | Python'",
    )
    bio = models.TextField(blank=True, help_text="Longer 'About me' text shown on the home page.")
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    resume = models.FileField(upload_to="resume/", blank=True, null=True, help_text="Upload a PDF resume/CV.")

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SkillCategory(models.Model):
    name = models.CharField(max_length=80, unique=True, help_text="e.g. Languages, Cloud & Infra, Data Engineering")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
