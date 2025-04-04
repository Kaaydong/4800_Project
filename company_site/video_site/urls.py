from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("bookmarks", views.bookmarks_page, name="bookmarks_page"),
    path('watch/<int:movie_id>/', views.movie_player, name='movie_player'),
]