from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("bookmarks", views.bookmarks_page, name="bookmarks_page"),
]