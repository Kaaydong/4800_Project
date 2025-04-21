from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from video_site.models import Movie, Genre
from user_forms.models import Settings
from datetime import date

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.genre = Genre.objects.create(genre="Action")
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Just a test",
            poster_url="poster.jpg",
            movie_file_url="movie/test/index.m3u8",
            age_restriction=1,
            release_date=date.today(),
            duration_seconds=1200,
            created_at=date.today(),
            activated_at=date.today(),
            modified_at=date.today()
        )
        Settings.objects.create(user_key=self.user, max_age_restriction=18)

    @patch('video_site.views.ML.MovieListing')
    def test_landing_page_guest(self, MockListing):
        MockListing.return_value.getRandomMovies.return_value = ['Random', []]
        MockListing.return_value.getTopDaily.return_value = ['Daily', []]
        MockListing.return_value.getTopWeekly.return_value = ['Weekly', []]
        MockListing.return_value.getTopAnnually.return_value = ['Yearly', []]
        MockListing.return_value.getMoviesForKids.return_value = ['Kids', []]
        MockListing.return_value.getMoviesForTeens.return_value = ['Teens', []]

        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/landing_page.html')

    @patch('video_site.views.ML.MovieListing')
    def test_landing_page_authenticated(self, MockListing):
        self.client.login(username='testuser', password='testpass')
        MockListing.return_value.getUserRecommended.return_value = ['Recommended', []]
        MockListing.return_value.getTopDaily.return_value = ['Daily', []]
        MockListing.return_value.getTopWeekly.return_value = ['Weekly', []]
        MockListing.return_value.getTopAnnually.return_value = ['Yearly', []]
        MockListing.return_value.getMoviesForKids.return_value = ['Kids', []]
        MockListing.return_value.getMoviesForTeens.return_value = ['Teens', []]

        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)

    @patch('video_site.views.ML.MovieListing')
    def test_bookmarks_page_redirect_if_guest(self, MockListing):
        response = self.client.get(reverse('bookmarks_page'))
        self.assertRedirects(response, '/users/login')

    @patch('video_site.views.ML.MovieListing')
    def test_movie_player_returns_404_if_movie_missing(self, MockListing):
        self.client.login(username='testuser', password='testpass')
        MockListing.return_value.getMovieById.return_value = None
        response = self.client.get(reverse('movie_player', args=[9999]))
        self.assertEqual(response.status_code, 404)

    @patch('video_site.views.ML.MovieListing')
    def test_movie_player_returns_page_if_movie_exists(self, MockListing):
        self.client.login(username='testuser', password='testpass')
        MockListing.return_value.getMovieById.return_value = (
            {'id': self.movie.movie_id}, 'PG', '2h', ['Action'], False
        )
        response = self.client.get(reverse('movie_player', args=[self.movie.movie_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/movie_player.html')

    def test_serve_hls_playlist_404_if_not_found(self):
        response = self.client.get(reverse('serve_hls_playlist', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_serve_hls_segment_404_if_not_found(self):
        response = self.client.get(reverse('serve_hls_segment', args=[9999, 'missing.ts']))
        self.assertEqual(response.status_code, 404)

    # @patch('video_site.views.ML.MovieListing')
    # def test_search_view_guest(self, MockListing):
    #     # Setup: Add genre to prevent empty genre list in context
    #     Genre.objects.create(genre="Comedy")

    #     # Simulate expected return: ['Search Results', [list of dummy movies]]
    #     MockListing.return_value.getMoviesByQuery.return_value = ['Search Results', [{'title': 'Mock Movie'}]]
        
    #     response = self.client.get(reverse('search'), {
    #         'query': 'test',
    #         'genre_filter': self.genre.genre_id  # ensure genre exists
    #     })

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'video_site/search_page.html')
    #     self.assertIn('RESULTS', response.context)
    #     self.assertTrue(response.context['RESULTS_FOUND'])
