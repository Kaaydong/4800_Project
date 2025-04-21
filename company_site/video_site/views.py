import copy
import os 
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import FileResponse, HttpResponse

from django.conf import settings
from user_forms import models

from . import models as data
from .classes import MovieListing as ML

# Render Landing Webpage
def landing_page(request):
    if request.user.is_authenticated:
        # Retrieve User info
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)   

        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "/users/logout"]
        account_settings = [user_settings.max_age_restriction]
        account_features = True

        # Generate Movie Lists with User Preferences
        ml = ML.MovieListing(user_settings.max_age_restriction, request.user.id)

        generated_movie_lists = [] # Format = ['name', movie_data]
        generated_movie_lists.append(ml.getUserRecommended())

    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["/users/login", "/users/register"]
        account_settings = [1]
        account_features = False

        # Generate Movie Lists without User Preferences
        ml = ML.MovieListing()

        generated_movie_lists = [] # Format = ['name', movie_data]
        generated_movie_lists.append(ml.getRandomMovies())

    # Add more categories

    generated_movie_lists.append(ml.getTopDaily())
    generated_movie_lists.append(ml.getTopWeekly())
    generated_movie_lists.append(ml.getTopAnnually())
    generated_movie_lists.append(ml.getMoviesForKids())
    generated_movie_lists.append(ml.getMoviesForTeens())

    return render(request, 'video_site/landing_page.html',
                  {'ACCOUNT_INFO': account_info,
                   'ACCOUNT_LINKS': account_links,
                   'ACCOUNT_SETTINGS': account_settings,
                   'ACCOUNT_FEATURES': account_features,
                   'MOVIE_LIST': generated_movie_lists,
                   })

# Render Bookmarks Webpage
def bookmarks_page(request):
    if request.user.is_authenticated:
        # Retrieve User info
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)       

        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "/users/logout"]
        account_settings = [user_settings.max_age_restriction]
        account_features = True

        # Generate Movie Lists with User Preferences
        ml = ML.MovieListing(user_settings.max_age_restriction, request.user.id)
        generated_movie_lists = [] # Format = ['name', movie_data]
        generated_movie_lists.append(ml.getBookmarkedMovies())

    else:
        return redirect("/users/login")
    
    return render(request, 'video_site/bookmarks_page.html',
                  {'ACCOUNT_INFO': account_info,
                   'ACCOUNT_LINKS': account_links,
                   'ACCOUNT_SETTINGS': account_settings,
                   'ACCOUNT_FEATURES': account_features,
                   'MOVIE_LIST': generated_movie_lists,
                   })

# Render Movie Player Webpage
def movie_player(request, movie_id):
    if request.user.is_authenticated:
        # Retrieve User info
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)     

        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "/users/logout"]
        account_settings = [user_settings.max_age_restriction]
        account_features = True

        # Create Movie Listing
        ml = ML.MovieListing(user_settings.max_age_restriction)

    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["/users/login", "/users/register"]
        account_settings = [1]
        account_features = False

        # Create Movie Listing
        ml = ML.MovieListing()

    # Fetch the movie data
    formatted_data = ml.getMovieById(movie_id)

    # Return 404 if requested movie doesn't exist
    if not formatted_data:
        return render(request, 'video_site/404.html', status=404)
    
    hls_playlist_url = reverse('serve_hls_playlist', args=[movie_id])

    return render(request, 'video_site/movie_player.html',
                  {'ACCOUNT_INFO': account_info,
                   'ACCOUNT_LINKS': account_links,
                   'ACCOUNT_SETTINGS': account_settings,
                   'ACCOUNT_FEATURES': account_features,
                   'HLS_URL': hls_playlist_url,
                   'MOVIE_DATA': formatted_data[0],
                   'AGE_RATING': formatted_data[1],
                   'DURATION': formatted_data[2],
                   'GENRES': formatted_data[3],
                   'BOOKMARKED': formatted_data[4],
                   })

# Serve Movie given movie ID
def serve_hls_playlist(request, movie_id):
    try:
        movie = get_object_or_404(data.Movie, pk=movie_id)
        hls_playlist_path = settings.BASE_DIR / "videos" / movie.movie_file_url

        with open(hls_playlist_path, 'r') as m3u8_file:
            m3u8_content = m3u8_file.read()

        base_url = request.build_absolute_uri('/') 
        serve_hls_segment_url = base_url +"serve_hls_segment/" + str(movie_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)

        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')
    
    except (data.Movie.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)

# Serve a HLS segement of a movie
def serve_hls_segment(request, movie_id, segment_name):
    try:
        movie = get_object_or_404(data.Movie, pk=movie_id)
        hls_playlist_path = settings.BASE_DIR / "videos" / movie.movie_file_url

        hls_directory = os.path.dirname(hls_playlist_path)
        segment_path = os.path.join(hls_directory, segment_name)

        # Serve the HLS segment as a binary file response
        return FileResponse(open(segment_path, 'rb'))
    except (data.Movie.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS segment not found", status=404)
    


def search_view(request):
    # Retrieve values from user input
    query = request.GET.get('query')
    filter = request.GET.get('genre_filter')
    results = []

    # Turn genre_id from filter to int
    #   filter == None during first visit
    #   filter == -1 if filter is set to None and user presses search
    if filter:
        filter = int(filter)

    # Get required rendering information    
    if request.user.is_authenticated:
        # Retrieve User info
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)   

        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "/users/logout"]
        account_settings = [user_settings.max_age_restriction]
        account_features = True

        ml = ML.MovieListing(user_settings.max_age_restriction, request.user.id)

    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["/users/login", "/users/register"]
        account_settings = [1]
        account_features = False

        ml = ML.MovieListing()

    # Get a List of genres for the filter option
    genres = data.Genre.objects.all()

    # Query database for movies matching the input query and genre filter
    results_found = False
    if query or filter:
        results = [ml.getMoviesByQuery(query, filter)]
        if len(results[0][1]) != 0:
            results_found = True

    return render(request, 'video_site/search_page.html',
                {'ACCOUNT_INFO': account_info,
                'ACCOUNT_LINKS': account_links,
                'ACCOUNT_SETTINGS': account_settings,
                'ACCOUNT_FEATURES': account_features,
                'GENRES': genres,
                'QUERY': query, 
                'PAST_FILTER': filter,
                'RESULTS': results,
                'RESULTS_FOUND': results_found,
                })

    