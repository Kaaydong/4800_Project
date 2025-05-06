from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from django.http import HttpResponse

class VideoSiteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
    
    def test_landing_page_guest(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/landing_page.html')
        self.assertIn('ACCOUNT_INFO', response.context)

    @patch('video_site.modules.UserAccounts.UserFunctions.getUserById')
    @patch('video_site.modules.UserAccounts.UserFunctions.getUserSettingsByUser')
    @patch('video_site.modules.MovieRecs.MovieListing.MovieListing.returnListOfMovieLists')
    def test_landing_page_authenticated(self, mock_list, mock_get_settings, mock_get_user):
        self.client.login(username='testuser', password='password')
        mock_user = self.user
        mock_user_settings = type('obj', (object,), {'max_age_restriction': 4})()
        mock_get_user.return_value = mock_user
        mock_get_settings.return_value = mock_user_settings
        mock_list.return_value = []

        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/landing_page.html')

    def test_bookmarks_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('bookmarks_page'))
        self.assertRedirects(response, '/users/login')

    @patch('video_site.modules.UserAccounts.UserFunctions.getUserById')
    @patch('video_site.modules.UserAccounts.UserFunctions.getUserSettingsByUser')
    @patch('video_site.modules.Bookmarks.BookmarkListing.BookmarkListing.getBookmarkedMovies')
    def test_bookmarks_page_authenticated(self, mock_bookmarks, mock_get_settings, mock_get_user):
        self.client.login(username='testuser', password='password')
        mock_user = self.user
        mock_user_settings = type('obj', (object,), {'max_age_restriction': 4})()
        mock_get_user.return_value = mock_user
        mock_get_settings.return_value = mock_user_settings
        mock_bookmarks.return_value = []

        response = self.client.get(reverse('bookmarks_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/bookmarks_page.html')

    @patch('video_site.modules.UserAccounts.UserFunctions.getUserById')
    @patch('video_site.modules.UserAccounts.UserFunctions.getUserSettingsByUser')
    @patch('video_site.modules.WatchHistory.WatchHistoryListing.WatchHistoryListing.getWatchedMovies')
    def test_watch_history_authenticated(self, mock_history, mock_get_settings, mock_get_user):
        self.client.login(username='testuser', password='password')
        mock_user = self.user
        mock_user_settings = type('obj', (object,), {'max_age_restriction': 4})()
        mock_get_user.return_value = mock_user
        mock_get_settings.return_value = mock_user_settings
        mock_history.return_value = []

        response = self.client.get(reverse('watch_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/watch_history_page.html')

    def test_watch_history_redirect_guest(self):
        response = self.client.get(reverse('watch_history'))
        self.assertRedirects(response, '/users/login')

    @patch('video_site.modules.MovieData.MovieDataFunctions.getAllGenres')
    @patch('video_site.modules.Search.SearchListing.SearchListing.getMoviesByQuery')
    @patch('video_site.modules.UserAccounts.UserFunctions.getUserById')
    @patch('video_site.modules.UserAccounts.UserFunctions.getUserSettingsByUser')
    def test_search_view_authenticated_with_query(self, mock_get_settings, mock_get_user, mock_get_movies, mock_get_genres):
        self.client.login(username='testuser', password='password')

        mock_user = self.user
        mock_settings = type('obj', (object,), {'max_age_restriction': 4})()
        mock_get_user.return_value = mock_user
        mock_get_settings.return_value = mock_settings
        mock_get_genres.return_value = ['Action', 'Comedy']
        mock_get_movies.return_value = ("query", [])

        response = self.client.get(reverse('search') + '?query=test&genre_filter=1')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/search_page.html')
        self.assertFalse(response.context['RESULTS_FOUND'])


    @patch('video_site.modules.MovieData.MovieDataFunctions.getAllGenres')
    @patch('video_site.modules.Search.SearchListing.SearchListing.getMoviesByQuery')
    def test_search_view_guest(self, mock_search, mock_genres):
        mock_genres.return_value = ['Action']
        mock_search.return_value = ("query", [])

        response = self.client.get(reverse('search') + '?query=test&genre_filter=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/search_page.html')
        self.assertFalse(response.context['RESULTS_FOUND'])

    
    @patch('video_site.modules.MovieData.MovieDataFunctions.getAllMovieActorEntriesOfMovie')
    @patch('video_site.modules.MovieData.MovieDataFunctions.getMovieById')
    @patch('video_site.modules.WatchHistory.WatchHistoryFunctions.getWatchEntryByUserAndMovies')
    @patch('video_site.modules.UserAccounts.UserFunctions.getUserById')
    @patch('video_site.modules.UserAccounts.UserFunctions.getUserSettingsByUser')
    @patch('video_site.modules.MovieRecs.MovieListing.MovieListing.getMovieById')
    def test_movie_player_authenticated(self, mock_ml_data, mock_user_settings, mock_user, mock_watch, mock_moviedata, mock_actors):
        self.client.login(username='testuser', password='password')
        mock_user.return_value = self.user
        mock_user_settings.return_value = type('obj', (object,), {'max_age_restriction': 4})()
        mock_ml_data.return_value = ("movie", "PG", 120, ["Action"], True)
        mock_watch.return_value = type('obj', (object,), {'watch_progress': 10})()
        mock_moviedata.return_value = type('obj', (object,), {'file_duration_seconds': 100})()
        mock_actors.return_value = [
            type('obj', (object,), {'actor_key': type('obj', (object,), {'first_name': 'John', 'last_name': 'Doe'})()})
        ]

        response = self.client.get(reverse('movie_player', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/movie_player.html')
        self.assertIn('MOVIE_DATA', response.context)

    @patch('video_site.modules.MovieRecs.MovieListing.MovieListing.getMovieById')
    def test_movie_player_guest(self, mock_ml_data):
        mock_ml_data.return_value = ("movie", "PG", 100, ["Comedy"], False)

        response = self.client.get(reverse('movie_player', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_site/movie_player.html')

    @patch('video_site.modules.MoviePlayer.HlsFunctions.serve_hls_playlist')
    def test_serve_hls_playlist(self, mock_serve):
        mock_serve.return_value = HttpResponse("m3u8_content", content_type="application/vnd.apple.mpegurl")
        response = self.client.get(reverse('serve_hls_playlist', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"m3u8_content")

    @patch('video_site.modules.MoviePlayer.HlsFunctions.serve_hls_segment')
    def test_serve_hls_segment(self, mock_serve):
        mock_serve.return_value = HttpResponse("segment_data", content_type='application/vnd.apple.mpegurl')
        response = self.client.get(reverse('serve_hls_segment', args=[1, "segment.ts"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"segment_data")