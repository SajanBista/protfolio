from django.conf import settings


def site_meta(request):
    """Global template context: site owner info used in base.html (nav, footer, meta tags)."""
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_EMAIL": settings.SITE_EMAIL,
        "GITHUB_USERNAME": settings.GITHUB_USERNAME,
        "LINKEDIN_URL": settings.LINKEDIN_URL,
    }
