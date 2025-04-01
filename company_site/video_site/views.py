import copy
from django.shortcuts import render
from django.contrib.auth import logout, get_user_model
from django.shortcuts import redirect
from user_forms import models

from . import models as data
from .classes import MovieListing as ML

# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        user = get_user_model().objects.get(id=request.user.id)
        user_settings = models.Settings.objects.get(user_key=user)

        # Render info if User is logged in
        account_info = [request.user.username, "Settings", "Logout"]
        account_links = ["javascript:;", "users/logout"]
        account_settings = [user_settings.max_age_restriction]
    else:
        # Render info if Guest Account is being used
        account_info = ["Guest", "Login", "Register"]
        account_links = ["users/login", "users/register"]
        account_settings = [1]

    # Filter movies with an age restriction of 12 or under
    ForKids_movies = data.Movie.objects.filter(age_restriction__lte=2)

    return render(request, 'video_site/landing_page.html',
                  {'ACCOUNT_INFO': account_info,
                   'ACCOUNT_LINKS': account_links,
                   'ACCOUNT_SETTINGS': account_settings,
                   'TRENDING_DAILY': ML.MovieListing.getTopDaily(),
                   'TRENDING_MONTHLY': ML.MovieListing.getTopMonthly(),
                   'RANDOM_MOVIES': ML.MovieListing.getRandomMovies(),
                   'KIDS_MOVIES': ML.MovieListing.getMoviesForKids(),
                   'TEEN_MOVIES': ML.MovieListing.getMoviesForTeens(),
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
