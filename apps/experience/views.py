from django.shortcuts import render

from .models import Experience


def experience_list(request):
    return render(request, "experience/experience_list.html", {"experiences": Experience.objects.all()})
