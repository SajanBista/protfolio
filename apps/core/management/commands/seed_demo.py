from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.blog.models import BlogPost, Tag
from apps.core.models import Profile, Skill, SkillCategory
from apps.education.models import Education
from apps.experience.models import Experience
from apps.learning.models import LearningLog
from apps.projects.models import Project


class Command(BaseCommand):
    help = "Seed the database with realistic sample content so the site isn't empty on first run."

    def handle(self, *args, **options):
        profile = Profile.get_solo()
        profile.full_name = "Sajan Bista"
        profile.headline = "Data Engineer · APIs, Web Scraping & AWS"
        profile.bio = (
            "Data engineer focused on building reliable data pipelines, API integrations, "
            "and web scraping systems on AWS. Currently deepening my computer science "
            "foundations toward a master's degree while building this portfolio in public."
        )
        profile.location = "Nepal"
        profile.email = "sajanbista1030@gmail.com"
        profile.github_url = "https://github.com/"
        if not profile.avatar and (Path(settings.MEDIA_ROOT) / "profile" / "profile.jpg").exists():
            profile.avatar.name = "profile/profile.jpg"
        profile.save()
        self.stdout.write(self.style.SUCCESS("Profile seeded."))

        skills = {
            "Languages": ["Python", "SQL", "JavaScript"],
            "Data Engineering": ["ETL Pipelines", "Apache Airflow", "Pandas", "dbt"],
            "Cloud & Infra": ["AWS Lambda", "AWS S3", "AWS EC2", "Docker"],
            "Web & APIs": ["Django", "REST APIs", "Web Scraping", "BeautifulSoup/Scrapy"],
        }
        for i, (cat_name, skill_names) in enumerate(skills.items()):
            category, _ = SkillCategory.objects.get_or_create(name=cat_name, defaults={"order": i})
            for j, skill_name in enumerate(skill_names):
                Skill.objects.get_or_create(category=category, name=skill_name, defaults={"order": j})
        self.stdout.write(self.style.SUCCESS("Skills seeded."))

        project, _ = Project.objects.get_or_create(
            title="API-Driven Web Scraping Actor",
            defaults={
                "summary": "A scheduled scraping actor that extracts structured data from target sites and pushes it through a REST API into cloud storage.",
                "description": (
                    "Built a configurable web scraping actor that runs on a schedule, "
                    "handles pagination and rate limiting, and normalizes results before "
                    "pushing them through an API layer into AWS S3 for downstream processing.\n\n"
                    "## Highlights\n"
                    "- Retry/backoff handling for flaky targets\n"
                    "- Structured JSON output validated against a schema\n"
                    "- Deployed as a containerized job on AWS"
                ),
                "tech_stack": "Python, Requests, BeautifulSoup, AWS Lambda, AWS S3, Docker",
                "is_featured": True,
                "order": 0,
            },
        )
        Project.objects.get_or_create(
            title="ETL Pipeline for Analytics Warehouse",
            defaults={
                "summary": "A batch ETL pipeline that ingests raw data, transforms it, and loads it into a warehouse for analytics.",
                "description": "Ingests data from multiple sources, applies transformations, and loads clean tables into a warehouse for BI dashboards.",
                "tech_stack": "Python, SQL, Airflow, PostgreSQL",
                "is_featured": True,
                "order": 1,
            },
        )
        self.stdout.write(self.style.SUCCESS("Projects seeded."))

        tag, _ = Tag.objects.get_or_create(name="AWS")
        post, created = BlogPost.objects.get_or_create(
            title="Why I'm Building My Portfolio on Django",
            defaults={
                "excerpt": "A quick look at why I chose a Django backend, Supabase for the future, and a learning log tied to GitHub.",
                "content": (
                    "As a data engineer, I wanted a portfolio that's more than a static page — "
                    "one backed by a real backend I control.\n\n"
                    "## Why Django\n"
                    "It's a framework I already know, it ships with a free admin panel for "
                    "managing content, and it scales cleanly from SQLite locally to Postgres "
                    "(via Supabase) in production.\n\n"
                    "## What's next\n"
                    "Supabase for the database, a learning log tied to GitHub issues and "
                    "branches, and eventually a proper deployment."
                ),
                "status": BlogPost.Status.PUBLISHED,
            },
        )
        if created:
            post.tags.add(tag)
        self.stdout.write(self.style.SUCCESS("Blog post seeded."))

        Education.objects.get_or_create(
            institution="University (update in admin)",
            degree="Bachelor's Degree",
            defaults={
                "field_of_study": "Computer Science / Information Technology",
                "start_date": date(2019, 9, 1),
                "end_date": date(2023, 6, 1),
                "description": "Foundational coursework in programming, databases, and systems.",
                "order": 1,
            },
        )
        Education.objects.get_or_create(
            institution="University (update in admin)",
            degree="Master's Degree",
            defaults={
                "field_of_study": "Computer Science",
                "start_date": date(2026, 1, 1),
                "is_ongoing": True,
                "description": "Pursuing graduate-level computer science coursework alongside professional work.",
                "order": 0,
            },
        )
        self.stdout.write(self.style.SUCCESS("Education seeded."))

        Experience.objects.get_or_create(
            company="Update in admin",
            role="Data Engineer",
            defaults={
                "location": "Remote",
                "employment_type": "Full-time",
                "start_date": date(2023, 7, 1),
                "is_current": True,
                "description": (
                    "Building data pipelines, API integrations, and web scraping systems on AWS.\n\n"
                    "- Designed and maintained ETL pipelines processing large datasets\n"
                    "- Built API-driven scraping actors for structured data extraction\n"
                    "- Deployed and monitored workloads on AWS"
                ),
                "order": 0,
            },
        )
        self.stdout.write(self.style.SUCCESS("Experience seeded."))

        LearningLog.objects.get_or_create(
            title="Set up the portfolio's Django backend",
            defaults={
                "summary": "Scaffolded the Django project structure: apps for blog, projects, education, experience, and learning.",
                "notes": (
                    "Today I set up the backend architecture for my portfolio site using Django.\n\n"
                    "- Split content into dedicated apps (blog, projects, education, experience, learning)\n"
                    "- Wired up the Django admin so all content is manageable without touching code\n"
                    "- Planned the GitHub integration for the learning log ticket system"
                ),
                "topic": "Django",
                "date": date.today(),
                "status": LearningLog.Status.DONE,
            },
        )
        self.stdout.write(self.style.SUCCESS("Learning log seeded."))

        self.stdout.write(self.style.SUCCESS("\nDemo data seeding complete."))
