from django.contrib import admin

# Register your models here.
from .models import Movie, Genre, Actor, MovieActorEntry, MovieGenreEntry, WatchEntry, BookmarkEntry

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(MovieActorEntry)
admin.site.register(MovieGenreEntry)
admin.site.register(WatchEntry)
admin.site.register(BookmarkEntry)
