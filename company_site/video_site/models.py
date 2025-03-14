from django.db import models
from django.contrib.auth import get_user_model

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024)
    description = models.TextField()
    poster_url = models.CharField(max_length=2048)
    movie_file_url = models.CharField(max_length=2048)
    age_restriction = models.IntegerField(default=1)
    release_date = models.DateField()
    duration_seconds = models.IntegerField()
    created_at = models.DateField()
    activated_at = models.DateField()
    modified_at = models.DateField()

    def __str__(self):
        return self.title
    

class MovieStatistics(models.Model):
    movie_stats_id = models.AutoField(primary_key=True)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(default=-1)
    rating_count = models.IntegerField(default=0)
    views_overall = models.IntegerField(default=0)
    views_daily = models.IntegerField(default=0)
    views_weekly = models.IntegerField(default=0)
    views_monthly = models.IntegerField(default=0)
    views_annually = models.IntegerField(default=0)


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=256)

    def __str__(self):
        return self.genre
    

class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=512)
    middle_name = models.CharField(max_length=512)
    last_name = models.CharField(max_length=512)

    def __str__(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name 


class MovieActorEntry(models.Model):
    movie_genre_entry_id = models.AutoField(primary_key=True)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor_key = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.actor_key)


class MovieGenreEntry(models.Model):
    movie_genre_entry_id = models.AutoField(primary_key=True)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre_key = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.genre_key)


class WatchEntry(models.Model):
    watch_entry_id = models.AutoField(primary_key=True)
    user_key = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_progress = models.FloatField(default=0)
    updated_at = models.DateField()

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.user_key)
    

class BookmarkEntry(models.Model):
    bookmark_entry_id = models.AutoField(primary_key=True)
    user_key = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie_key) + " | " + str(self.user_key)


class RatingEntry(models.Model):
    rating_entry_id = models.AutoField(primary_key=True)
    user_key = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating_value = models.FloatField(default=-1)

    def __str__(self):
        return "Rating | " + str(self.movie_key) + " | " + str(self.user_key)
