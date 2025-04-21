from django.test import TestCase

from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import *

class ModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="A test movie",
            poster_url="http://example.com/poster.jpg",
            movie_file_url="http://example.com/movie.mp4",
            age_restriction=1,
            release_date=timezone.now().date(),
            duration_seconds=7200,
            created_at=timezone.now().date(),
            activated_at=timezone.now().date(),
            modified_at=timezone.now().date()
        )
        self.genre = Genre.objects.create(genre="Action")
        self.actor = Actor.objects.create(first_name="John", middle_name="H.", last_name="Doe")

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Test Movie")

    def test_movie_statistics_creation(self):
        stats = MovieStatistics.objects.create(movie_key=self.movie, rating=4.5, rating_count=10)
        self.assertEqual(str(stats), "Test Movie | Stats")

    def test_genre_str(self):
        self.assertEqual(str(self.genre), "Action")

    def test_actor_str(self):
        self.assertEqual(str(self.actor), "John H. Doe")

    def test_movie_actor_entry_str(self):
        entry = MovieActorEntry.objects.create(movie_key=self.movie, actor_key=self.actor)
        self.assertIn("Test Movie", str(entry))
        self.assertIn("John H. Doe", str(entry))

    def test_movie_genre_entry_str(self):
        entry = MovieGenreEntry.objects.create(movie_key=self.movie, genre_key=self.genre)
        self.assertIn("Test Movie", str(entry))
        self.assertIn("Action", str(entry))

    def test_watch_entry_str(self):
        watch = WatchEntry.objects.create(
            user_key=self.user,
            movie_key=self.movie,
            watch_progress=50.0,
            updated_at=timezone.now().date()
        )
        self.assertIn("Test Movie", str(watch))
        self.assertIn("testuser", str(watch))

    def test_bookmark_entry_str(self):
        bookmark = BookmarkEntry.objects.create(user_key=self.user, movie_key=self.movie)
        self.assertIn("Test Movie", str(bookmark))
        self.assertIn("testuser", str(bookmark))

    def test_rating_entry_str(self):
        rating = RatingEntry.objects.create(user_key=self.user, movie_key=self.movie, rating_value=4.0)
        self.assertIn("Rating | Test Movie", str(rating))
        self.assertIn("testuser", str(rating))
