from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_screen, name="home_screen"),
    path("crew", views.crew, name="crew"),
    path("meeting_logs", views.meeting_logs, name="meeting_logs"),
]