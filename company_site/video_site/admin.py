from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Settings)
admin.site.register(models.Movie)
admin.site.register(models.Genre)
admin.site.register(models.Actor)
admin.site.register(models.MovieActorEntry)
admin.site.register(models.MovieGenreEntry)
admin.site.register(models.WatchEntry)
admin.site.register(models.BookmarkEntry)
