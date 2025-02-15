from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField(default=1)
    random = models.IntegerField(default=0)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    password_hash = models.CharField(max_length=256)
    created_at = models.DateField()
    modified_at = models.DateField()

    def __str__(self):
        return self.username


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024)
    description = models.TextField()
    release_data = models.DateField()
    duration_mins = models.FloatField()
    rating = models.FloatField(default=-1)
    rating_quantity = models.IntegerField(default=0)
    poster_url = models.CharField(max_length=2048)
    trailer_url = models.CharField(max_length=2048)
    created_at = models.DateField()
    modified_at = models.DateField()

    def __str__(self):
        return self.title


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=256)

    def __str__(self):
        return self.genre


class MovieEntry(models.Model):
    movie_entry_id = models.AutoField(primary_key=True)
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre_key = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_key


class WatchEntry(models.Model):
    watch_entry_id = models.AutoField(primary_key=True)
    user_key = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_entry_key = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_percentage = models.FloatField(default=0)
    updated_at = models.DateField()

    def __str__(self):
        return self.movie_entry_key


class BookmarkEntry(models.Model):
    bookmark_entry_id = models.AutoField(primary_key=True)
    user_key = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_entry_key = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_entry_key


