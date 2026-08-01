from django.shortcuts import get_object_or_404, render

from .models import LearningLog


def log_list(request):
    logs = LearningLog.objects.all()

    topic = request.GET.get("topic")
    if topic:
        logs = logs.filter(topic=topic)

    status = request.GET.get("status")
    if status:
        logs = logs.filter(status=status)

    context = {
        "logs": logs,
        "topics": LearningLog.objects.exclude(topic="").values_list("topic", flat=True).distinct(),
        "status_choices": LearningLog.Status.choices,
        "active_topic": topic,
        "active_status": status,
    }
    return render(request, "learning/log_list.html", context)


def log_detail(request, slug):
    entry = get_object_or_404(LearningLog, slug=slug)
    return render(request, "learning/log_detail.html", {"entry": entry})
