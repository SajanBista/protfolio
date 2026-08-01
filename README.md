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

## Deployment

Not yet configured. `whitenoise` is already wired in for static file serving,
so the app is close to deploy-ready for platforms like Railway, Fly.io, or a
VPS — set `DEBUG=False`, a real `SECRET_KEY`, and `ALLOWED_HOSTS` in the
production environment.
