"""
GitHub integration for the Learning Log.

Each LearningLog entry has a ticket number (LEARN-0001) and a suggested branch
name (learn/learn-0001-title-slug). This module turns a LearningLog entry into
a real GitHub issue via the REST API, so daily learning activity shows up as
issues on a GitHub repo that can be closed by commits on the matching branch.

Setup: set GITHUB_TOKEN (a fine-grained PAT with Issues read/write on the
target repo) and GITHUB_REPO ("username/repo") in your .env file.
"""

from dataclasses import dataclass

import requests
from django.conf import settings

GITHUB_API_URL = "https://api.github.com"


class GitHubNotConfigured(Exception):
    pass


class GitHubAPIError(Exception):
    pass


@dataclass
class IssueResult:
    number: int
    url: str


def _headers():
    return {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def is_configured() -> bool:
    return bool(settings.GITHUB_TOKEN and settings.GITHUB_REPO)


def create_issue_for_learning_log(entry) -> IssueResult:
    """
    Create a GitHub issue for a LearningLog entry.

    `entry` is an apps.learning.models.LearningLog instance. Does not save the
    entry itself — the caller is responsible for persisting the returned
    issue number/url back onto the model.
    """
    if not is_configured():
        raise GitHubNotConfigured(
            "Set GITHUB_TOKEN and GITHUB_REPO in your .env file before creating GitHub issues."
        )

    url = f"{GITHUB_API_URL}/repos/{settings.GITHUB_REPO}/issues"
    payload = {
        "title": f"[{entry.ticket_number}] {entry.title}",
        "body": (
            f"{entry.summary}\n\n"
            f"{entry.notes}\n\n"
            f"---\n"
            f"**Topic:** {entry.topic or 'n/a'}\n"
            f"**Suggested branch:** `{entry.branch_name}`\n"
            f"**Date:** {entry.date}"
        ),
        "labels": ["learning"] + ([entry.topic] if entry.topic else []),
    }
    response = requests.post(url, json=payload, headers=_headers(), timeout=15)
    if response.status_code >= 300:
        raise GitHubAPIError(f"GitHub API error ({response.status_code}): {response.text}")

    data = response.json()
    return IssueResult(number=data["number"], url=data["html_url"])
