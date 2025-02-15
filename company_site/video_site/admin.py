from django.contrib import admin

# Register your models here.
from .models import Test, User, Movie, Genre, MovieEntry, WatchEntry, BookmarkEntry

admin.site.register(Test)
admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MovieEntry)
admin.site.register(WatchEntry)
admin.site.register(BookmarkEntry)
