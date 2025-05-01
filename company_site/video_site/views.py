from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .modules.UserAccounts import UserFunctions as uf

# Generate info for the toolbar, results depend on user authentication status
def generateToolbarInfo(isAuthenticated, request=None, user_settings=None):
    if isAuthenticated:
        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "/users/logout"]
        account_settings = [user_settings.max_age_restriction]
        account_features = True
    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["/users/login", "/users/register"]
        account_settings = [1]
        account_features = False
    
    return [account_info, account_links, account_settings, account_features]


# ====================================== Render Landing Webpage ============================================= #
from .modules.MovieRecs import MovieListing as ML

def landing_page(request):
    if request.user.is_authenticated:
        # Retrieve User info
        user = uf.getUserById(request.user.id)
        user_settings = uf.getUserSettingsByUser(user)
        age_restriction = user_settings.max_age_restriction
        
        # Render info if User is logged in
        toolBarInfo = generateToolbarInfo(True, request, user_settings)

        # Generate Movie Lists with User Preferences
        ml = ML.MovieListing(age_restriction, request.user.id)
    else:
        # Render info if Guest Account is being used
        toolBarInfo = generateToolbarInfo(False)

        # Generate Movie Lists without User Preferences
        ml = ML.MovieListing()


    generated_movie_lists = ml.returnListOfMovieLists()

    return render(request, 'video_site/landing_page.html',
                  {'ACCOUNT_INFO': toolBarInfo[0],
                   'ACCOUNT_LINKS': toolBarInfo[1],
                   'ACCOUNT_SETTINGS': toolBarInfo[2],
                   'ACCOUNT_FEATURES': toolBarInfo[3],
                   'MOVIE_LIST': generated_movie_lists,
                   })


# ====================================== Render Bookmarks Webpage ============================================= #
from .modules.Bookmarks.BookmarkListing import BookmarkListing

def bookmarks_page(request):
    if request.user.is_authenticated:
        # Retrieve User info
        user = uf.getUserById(request.user.id)
        user_settings = uf.getUserSettingsByUser(user)         

        # Render info if User is logged in
        toolBarInfo = generateToolbarInfo(True, request, user_settings)

        # Generate Movie Lists with User Preferences
        listing = BookmarkListing(user_settings.max_age_restriction, request.user.id)
        generated_movie_lists = [listing.getBookmarkedMovies()]

    else:
        # Deny access if user is unauthenticated
        return redirect("/users/login")
    
    return render(request, 'video_site/bookmarks_page.html',
                  {'ACCOUNT_INFO': toolBarInfo[0],
                   'ACCOUNT_LINKS': toolBarInfo[1],
                   'ACCOUNT_SETTINGS': toolBarInfo[2],
                   'ACCOUNT_FEATURES': toolBarInfo[3],
                   'MOVIE_LIST': generated_movie_lists,
                   })

# ====================================== Render Watch History Webpage ============================================= #
from .modules.WatchHistory.WatchHistoryListing import WatchHistoryListing

def watch_history_page(request):
    if request.user.is_authenticated:
        # Retrieve User info
        user = uf.getUserById(request.user.id)
        user_settings = uf.getUserSettingsByUser(user)        

        # Render info if User is logged in
        toolBarInfo = generateToolbarInfo(True, request, user_settings)

        # Generate Movie Lists with User Preferences
        listing = WatchHistoryListing(user_settings.max_age_restriction, request.user.id)
        generated_movie_lists = [listing.getWatchedMovies()]

    else:
        # Deny access if user is unauthenticated
        return redirect("/users/login")
    
    return render(request, 'video_site/watch_history_page.html',
                  {'ACCOUNT_INFO': toolBarInfo[0],
                   'ACCOUNT_LINKS': toolBarInfo[1],
                   'ACCOUNT_SETTINGS': toolBarInfo[2],
                   'ACCOUNT_FEATURES': toolBarInfo[3],
                   'MOVIE_LIST': generated_movie_lists,
                   })


# ====================================== Render Watch History Webpage ============================================= #
from .modules.Search.SearchListing import SearchListing
from .modules.MovieData import MovieDataFunctions

# Movie Search Page Functionality
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
        user = uf.getUserById(request.user.id)
        user_settings = uf.getUserSettingsByUser(user)    

        # Render info if User is logged in
        toolBarInfo = generateToolbarInfo(True, request, user_settings)

        sl = SearchListing(user_settings.max_age_restriction, request.user.id)
    else:
        # Render info if User is logged in
        toolBarInfo = generateToolbarInfo(False)

        sl = SearchListing()

    # Get a List of genres for the filter option
    genres = MovieDataFunctions.getAllGenres()

    # Query database for movies matching the input query and genre filter
    results_found = False
    if query or filter:
        results = [sl.getMoviesByQuery(query, filter)]
        if len(results[0][1]) != 0:
            results_found = True

    return render(request, 'video_site/search_page.html',
                {'ACCOUNT_INFO': toolBarInfo[0],
                'ACCOUNT_LINKS': toolBarInfo[1],
                'ACCOUNT_SETTINGS': toolBarInfo[2],
                'ACCOUNT_FEATURES': toolBarInfo[3],
                'GENRES': genres,
                'QUERY': query, 
                'PAST_FILTER': filter,
                'RESULTS': results,
                'RESULTS_FOUND': results_found,
                })

    


# ====================================== Render Movie Player Webpage ============================================= #
from .modules.WatchHistory import WatchHistoryFunctions
from .modules.MovieData import MovieDataFunctions


def movie_player(request, movie_id):
    watch_progress = 0
    if request.user.is_authenticated:
        # Retrieve User info
        user = uf.getUserById(request.user.id)
        user_settings = uf.getUserSettingsByUser(user)      

        # Render info if User is logged in
        toolBarInfo = generateToolbarInfo(True, request, user_settings)

        # Create Movie Listing
        ml = ML.MovieListing(user_settings.max_age_restriction)

        # Get watch progress of user
        try:
            watch_progress = WatchHistoryFunctions.getWatchEntryByUserAndMovies(user, movie_id).watch_progress
            if watch_progress >= MovieDataFunctions.getMovieById(movie_id).file_duration_seconds:
                watch_progress = 0
        except:
            watch_progress = 0

    else:
        # Render info if Guest Account is being used
        toolBarInfo = generateToolbarInfo(False)

        # Create Movie Listing
        ml = ML.MovieListing()

    # Fetch the movie data
    formatted_data = ml.getMovieById(movie_id)

    # Fetch actor data
    actors = MovieDataFunctions.getAllMovieActorEntriesOfMovie(movie_id)
    actor_list = []
    for actor in actors:
        actor_list.append(actor.actor_key.first_name + " " + actor.actor_key.last_name)

    # Return 404 if requested movie doesn't exist
    if not formatted_data:
        return render(request, 'video_site/404.html', status=404)
    
    hls_playlist_url = reverse('serve_hls_playlist', args=[movie_id])

    return render(request, 'video_site/movie_player.html',
                  {'ACCOUNT_INFO': toolBarInfo[0],
                   'ACCOUNT_LINKS': toolBarInfo[1],
                   'ACCOUNT_SETTINGS': toolBarInfo[2],
                   'ACCOUNT_FEATURES': toolBarInfo[3],
                   'HLS_URL': hls_playlist_url,
                   'WATCH_PROGRESS': watch_progress,
                   'ACTOR_LIST': actor_list,
                   'MOVIE_DATA': formatted_data[0],
                   'AGE_RATING': formatted_data[1],
                   'DURATION': formatted_data[2],
                   'GENRES': formatted_data[3],
                   'BOOKMARKED': formatted_data[4],
                   })


# ====================================== Render Movie Player Video Content ============================================= #
from .modules.MoviePlayer import HlsFunctions

# Serve Movie given movie ID
def serve_hls_playlist(request, movie_id):
    return HlsFunctions.serve_hls_playlist(request, movie_id)

# Serve a HLS segement of a movie
def serve_hls_segment(request, movie_id, segment_name):
    return HlsFunctions.serve_hls_segment(request, movie_id, segment_name)