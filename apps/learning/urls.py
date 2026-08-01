from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path("", views.log_list, name="list"),
    path("<slug:slug>/", views.log_detail, name="detail"),
]
