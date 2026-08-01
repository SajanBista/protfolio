from django.shortcuts import render

from apps.blog.models import BlogPost
from apps.education.models import Education
from apps.experience.models import Experience
from apps.projects.models import Project

from .models import Profile, SkillCategory


def home(request):
    context = {
        "profile": Profile.get_solo(),
        "skill_categories": SkillCategory.objects.prefetch_related("skills"),
        "featured_projects": Project.objects.filter(is_featured=True)[:4],
        "latest_posts": BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)[:3],
        "experiences": Experience.objects.all()[:3],
        "education": Education.objects.all()[:2],
    }
    return render(request, "core/home.html", context)
