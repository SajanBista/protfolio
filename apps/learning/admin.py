from django.contrib import admin, messages

from . import github
from .models import LearningLog


@admin.register(LearningLog)
class LearningLogAdmin(admin.ModelAdmin):
    list_display = ("ticket_number", "title", "topic", "status", "date", "github_issue_number")
    list_filter = ("status", "topic")
    search_fields = ("ticket_number", "title", "notes", "topic")
    readonly_fields = ("ticket_number", "branch_name", "github_issue_number", "github_issue_url")
    date_hierarchy = "date"
    actions = ["create_github_issue"]

    @admin.action(description="Create GitHub issue for selected learning log(s)")
    def create_github_issue(self, request, queryset):
        if not github.is_configured():
            self.message_user(
                request,
                "GITHUB_TOKEN / GITHUB_REPO are not set in .env — configure them first.",
                level=messages.ERROR,
            )
            return

        created, skipped, failed = 0, 0, 0
        for entry in queryset:
            if entry.github_issue_number:
                skipped += 1
                continue
            try:
                result = github.create_issue_for_learning_log(entry)
            except (github.GitHubNotConfigured, github.GitHubAPIError) as exc:
                failed += 1
                self.message_user(request, f"{entry.ticket_number}: {exc}", level=messages.ERROR)
                continue
            entry.github_issue_number = result.number
            entry.github_issue_url = result.url
            entry.save(update_fields=["github_issue_number", "github_issue_url"])
            created += 1

        self.message_user(
            request,
            f"Created {created} issue(s), skipped {skipped} (already linked), {failed} failed.",
            level=messages.SUCCESS if created else messages.WARNING,
        )
