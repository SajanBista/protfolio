"""
Django settings for config project (Sajan Bista's portfolio).
"""

from pathlib import Path

import dj_database_url
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-dev-key-change-me-in-production",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# Trusted origins for CSRF (needed once the site is served over HTTPS on a
# real domain, e.g. https://yourapp.onrender.com). Comma-separated.
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "storages",
    # Local apps
    "apps.core",
    "apps.blog",
    "apps.projects",
    "apps.education",
    "apps.experience",
    "apps.learning",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_meta",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#
# Local dev defaults to SQLite. To switch to Supabase (Postgres) later,
# just set DATABASE_URL in .env, e.g.:
# DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres

DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (user/admin-uploaded images: avatar, blog covers, project
# screenshots, resume, etc.)
#
# Locally this stays on disk. In production (most free hosts have an
# ephemeral filesystem), point it at a Supabase Storage bucket instead by
# setting SUPABASE_PROJECT_REF + SUPABASE_S3_* in .env — see .env.example.
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

SUPABASE_PROJECT_REF = config("SUPABASE_PROJECT_REF", default="")
SUPABASE_S3_ACCESS_KEY_ID = config("SUPABASE_S3_ACCESS_KEY_ID", default="")
SUPABASE_S3_SECRET_ACCESS_KEY = config("SUPABASE_S3_SECRET_ACCESS_KEY", default="")
SUPABASE_S3_BUCKET = config("SUPABASE_S3_BUCKET", default="media")
SUPABASE_S3_REGION = config("SUPABASE_S3_REGION", default="us-east-1")

USE_SUPABASE_STORAGE = bool(
    SUPABASE_PROJECT_REF and SUPABASE_S3_ACCESS_KEY_ID and SUPABASE_S3_SECRET_ACCESS_KEY
)

if USE_SUPABASE_STORAGE:
    AWS_ACCESS_KEY_ID = SUPABASE_S3_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = SUPABASE_S3_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = SUPABASE_S3_BUCKET
    AWS_S3_REGION_NAME = SUPABASE_S3_REGION
    AWS_S3_ENDPOINT_URL = f"https://{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/s3"
    # Supabase serves public files from a different path than the S3 API
    # endpoint above, so URLs are built against this custom domain instead.
    # django-storages doesn't insert the bucket name when a custom domain is
    # set (it assumes the domain is already bucket-specific), so it's baked
    # into the domain here to match Supabase's path-style public URLs.
    AWS_S3_CUSTOM_DOMAIN = f"{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/object/public/{SUPABASE_S3_BUCKET}"
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False

STORAGES = {
    "default": {
        "BACKEND": (
            "storages.backends.s3.S3Storage"
            if USE_SUPABASE_STORAGE
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Site / owner info (used in templates & context processor) -------------
SITE_NAME = config("SITE_NAME", default="Sajan Bista")
SITE_TAGLINE = config("SITE_TAGLINE", default="Data Engineer")
SITE_EMAIL = config("SITE_EMAIL", default="")
GITHUB_USERNAME = config("GITHUB_USERNAME", default="")
LINKEDIN_URL = config("LINKEDIN_URL", default="")

# --- GitHub integration (Learning Log ticket -> issue/branch) --------------
# Create a fine-grained personal access token with "Issues: read/write"
# permission on the target repo and set these in your .env file.
GITHUB_TOKEN = config("GITHUB_TOKEN", default="")
GITHUB_REPO = config("GITHUB_REPO", default="")  # format: "username/repo"


# --- Production hardening ---------------------------------------------------
# Hosts like Render/Railway/PythonAnywhere terminate TLS at a proxy in front
# of the app, so Django needs to trust the X-Forwarded-Proto header to know
# a request was actually HTTPS (otherwise SECURE_SSL_REDIRECT loops forever).
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=604800, cast=int)  # 7 days
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
