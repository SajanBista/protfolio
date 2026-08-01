# Sajan Bista — Portfolio

Django-backed personal portfolio: Projects, Blog, Experience, Education, and a
Learning Log that ties daily learning activity to GitHub issues/branches via
ticket numbers (`LEARN-0001`, ...).

## Stack

- **Backend:** Django 5 (server-rendered templates, no separate frontend build)
- **Database:** SQLite locally → Supabase (Postgres) later via `DATABASE_URL`
- **Styling:** hand-written CSS (dark/light theme, no framework/build step)
- **Content:** managed entirely through the Django admin at `/admin/`

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then fill in values as needed

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `/admin/` to manage content
(profile, skills, projects, blog posts, experience, education, learning log).

## App structure

```
apps/
  core/        Profile/skills + home page
  blog/        Blog posts + tags
  projects/    Project showcase
  education/   Academic qualifications
  experience/  Work history
  learning/    Learning log (ticket numbers + GitHub integration)
```

## Learning Log → GitHub

Each `LearningLog` entry auto-generates:
- a **ticket number** (`LEARN-0001`, `LEARN-0002`, ...)
- a **suggested branch name** (`learn/learn-0001-title-slug`)

To push an entry to GitHub as a real issue:

1. In `.env`, set `GITHUB_TOKEN` (fine-grained PAT with Issues read/write on
   the target repo) and `GITHUB_REPO` (`username/repo`).
2. In the admin, select one or more Learning Log entries and run the
   **"Create GitHub issue for selected learning log(s)"** action.
3. The issue number/URL are saved back onto the entry and shown on its detail
   page. Create a local branch matching `branch_name` and commit your work
   there, referencing the issue.

## Moving to Supabase

Set `DATABASE_URL` in `.env` to your Supabase Postgres connection string,
then re-run `python manage.py migrate`. No code changes needed —
`dj-database-url` reads it automatically and falls back to SQLite if unset.

## Deployment (free: Render + Supabase)

The app is deploy-ready for a fully free stack: **Render** (web hosting,
`gunicorn` and `whitenoise` already wired in) plus **Supabase** (Postgres
database and S3-compatible object storage for uploaded media). Local disk is
only used as a fallback when the Supabase storage env vars aren't set, since
most free hosts wipe local disk on every deploy.

### 1. Supabase — database

1. Create a project at supabase.com (free tier).
2. Project Settings → Database → copy the connection string (use the
   "Session pooler" URI) into `DATABASE_URL`.

### 2. Supabase — media storage

1. In the same project, go to Storage → create a new **public** bucket
   (e.g. `media`).
2. Project Settings → API → under "S3 Connection", generate an access
   key pair.
3. Set in your environment: `SUPABASE_PROJECT_REF` (the `<ref>` in your
   project URL), `SUPABASE_S3_ACCESS_KEY_ID`, `SUPABASE_S3_SECRET_ACCESS_KEY`,
   `SUPABASE_S3_BUCKET` (bucket name), `SUPABASE_S3_REGION` (shown on that
   same S3 Connection panel).
4. Leave all of these blank and the app just uses local disk (fine for local
   dev).

### 3. Render — web app

1. Push this repo to GitHub, then create a new **Web Service** on
   render.com pointing at it (free tier).
2. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start command: leave default — Render picks up the `Procfile`
   (`gunicorn config.wsgi`).
4. Set environment variables: `SECRET_KEY` (generate a real random value),
   `DEBUG=False`, `ALLOWED_HOSTS=<yourapp>.onrender.com`,
   `CSRF_TRUSTED_ORIGINS=https://<yourapp>.onrender.com`, `DATABASE_URL`,
   and the `SUPABASE_*` vars from step 2.
5. Deploy, then use Render's **Shell** tab to run
   `python manage.py createsuperuser` once.

Free-tier caveats worth knowing: Render's free web service spins down after
~15 min idle (first request after that takes ~30–50s to wake up), and
Supabase's free Postgres pauses after a week of no activity (same kind of
wake-up delay on the next visit). Neither is a problem for a low-traffic
portfolio.
