from django.db import models
from pygments.lexer import default
from django.contrib.auth import get_user_model

class Settings(models.Model):
    user_key = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    safe_mode_enabled = models.BooleanField(default=False)

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024)
    description = models.TextField()
    poster_url = models.CharField(max_length=2048)
    age_restriction = models.IntegerField(default=1)
    release_date = models.DateField()
    duration_mins = models.FloatField()
    rating = models.FloatField(default=-1)
    rating_count = models.IntegerField(default=0)
    views_overall = models.IntegerField(default=0)
    views_daily = models.IntegerField(default=0)
    views_weekly = models.IntegerField(default=0)
    views_monthly = models.IntegerField(default=0)
    views_annually = models.IntegerField(default=0)
    created_at = models.DateField()
    modified_at = models.DateField()

    def __str__(self):
        return self.title


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=256)

    def __str__(self):
        return self.genre
    
class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    actor_name = models.CharField(max_length=1024)

    def __str__(self):
        return self.actor_name


class MovieActorEntry(models.Model):
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor_key = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.actor_key)


class MovieGenreEntry(models.Model):
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre_key = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.genre_key)


class WatchEntry(models.Model):
    watch_entry_id = models.AutoField(primary_key=True)
    user_key = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_progress = models.FloatField(default=0)
    user_rating = models.IntegerField(default=1)
    updated_at = models.DateField()

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.user_key)
    


class BookmarkEntry(models.Model):
    bookmark_entry_id = models.AutoField(primary_key=True)
    user_key = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.user_key)

