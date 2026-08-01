from django.contrib import admin

from .models import Education


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "start_date", "end_date", "is_ongoing", "order")
    list_editable = ("order",)
    list_filter = ("is_ongoing",)
