import copy
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from user_forms import models

from . import models as data
from .classes import MovieListing as ML

# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)
        user_settings = models.Settings.objects.get(user_key=user)        

        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "users/logout"]
        account_settings = [user_settings.max_age_restriction]

        # Generate Movie Lists with User Preferences
        ml = ML.MovieListing(user_settings.max_age_restriction)

        generated_movie_lists = [] # Format = ['name', movie_data]
        generated_movie_lists.append(ml.getUserRecommended(request.user.id))

    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["users/login", "users/register"]
        account_settings = [1]

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
                   'MOVIE_LIST': generated_movie_lists,
                   })

def movie_player(request, movie_id):
    # Authenticated user? Load settings.
    if request.user.is_authenticated:
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)
        ml = ML.MovieListing(user_settings.max_age_restriction)
    else:
        ml = ML.MovieListing()

    # Fetch the movie data
    movie_data = ml.getMovieById(movie_id)

    if not movie_data:
        return render(request, 'video_site/404.html', status=404)

    return render(request, 'video_site/movie_player.html', {
        'movie': movie_data
    })

def bookmarks_page(request):
    if request.user.is_authenticated:
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)

        account_settings = [user_settings.max_age_restriction]
        username = request.user.username

        bookmarks = data.BookmarkEntry.objects.filter(user_key=user)
        movies_list = []
        for movie in bookmarks:
            movies_list.append(data.Movie.objects.get(movie_id=movie.movie_key.movie_id))
        
        duration_list = []
        for movie in copy.deepcopy(movies_list):
            duration_string = ""
            
            hours = movie.duration_seconds // 3600
            if hours > 0:
                duration_string = str(movie.duration_seconds // 3600) + "h "
                
            duration_string += str(movie.duration_seconds // 60) + "m " + str(movie.duration_seconds % 60) + "s"
            duration_list.append(duration_string)

        movies_combined_list = []
        for m, d in zip(movies_list, duration_list):
            movies_combined_list.append([m, d])

    else:
        return redirect("/users/login")
    
    return render(request, "video_site/bookmarks_page.html",
                  {'ACCOUNT_USERNAME': username, 'ACCOUNT_SETTINGS': account_settings, 'ACCOUNT_BOOKMARKS': movies_combined_list})
