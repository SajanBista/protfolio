from datetime import date

from django.shortcuts import render

from apps.blog.models import BlogPost
from apps.education.models import Education
from apps.experience.models import Experience
from apps.projects.models import Project

from .models import Profile, SkillCategory


def home(request):
    experiences = Experience.objects.all()
    earliest_start = experiences.order_by("start_date").values_list("start_date", flat=True).first()
    years_experience = (date.today() - earliest_start).days // 365 if earliest_start else 0

    context = {
        "profile": Profile.get_solo(),
        "skill_categories": SkillCategory.objects.prefetch_related("skills"),
        "featured_projects": Project.objects.filter(is_featured=True)[:4],
        "latest_posts": BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)[:3],
        "experiences": experiences[:3],
        "education": Education.objects.all()[:2],
        "stats": {
            "projects": Project.objects.count(),
            "posts": BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED).count(),
            "years_experience": years_experience,
        },
    }
    return render(request, "core/home.html", context)
