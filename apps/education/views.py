from django.shortcuts import render

from .models import Education


def education_list(request):
    return render(request, "education/education_list.html", {"education_items": Education.objects.all()})
