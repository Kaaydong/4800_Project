from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("bookmarks", views.bookmarks_page, name="bookmarks_page"),
    path("watch_history", views.watch_history_page, name="watch_history"),
    path('search', views.search_view, name='search'),
    path('watch/<int:movie_id>/', views.movie_player, name='movie_player'),
    path('serve_hls_playlist/<int:movie_id>/', views.serve_hls_playlist, name='serve_hls_playlist'),
    path('serve_hls_segment/<int:movie_id>/<str:segment_name>/',views.serve_hls_segment, name='serve_hls_segment'),
]