import random
from .. import models as data

class MovieListing():

    # returns a movie as a tuple, with all of its required data
    # FORMAT = [movie, duration_formatted, restriction_formatted, genres_formatted]
    def generateMovieCardInfo(movie):
        duration = movie.duration_seconds
        restriction = movie.age_restriction
        genres = data.MovieGenreEntry.objects.filter(movie_key=movie.movie_id)

        restriction_formatted = ""
        if restriction == 1:
            restriction_formatted = " | G | "
        elif restriction == 2:
            restriction_formatted = " | PG | "
        elif restriction == 3:
            restriction_formatted = " | PG-13 | "
        elif restriction == 4:
            restriction_formatted = " | R | "
        else:
            restriction_formatted = " | NR | "

        duration_formatted = ""
        hours = duration // 3600
        if hours > 0:
            duration_formatted = str(duration // 3600) + "h "
            duration_formatted += str(duration // 60) + "m"
        else:
            duration_formatted = str(duration // 60) + "m "
            duration_formatted += str(duration % 60) + "s"

        genres_formatted = ""
        genres = genres[:3]
        for i in range(0, len(genres)):
            genres_formatted += genres[i].genre_key.genre
            if i < len(genres) - 1:
                genres_formatted += ", " 

        return [movie, restriction_formatted, duration_formatted, genres_formatted]

    # get top 10 daily movies
    @staticmethod
    def getTopDaily():
        movie_stats = data.MovieStatistics.objects.all()
        movie_stat_list = []
        for stat in movie_stats:
            movie_stat_list.append(stat)

        movie_stat_list.sort(key=lambda x: x.views_daily, reverse=True)
        movie_stat_list = movie_stat_list[:10]

        returned_list = []
        for stat in movie_stat_list:
            returned_list.append(MovieListing.generateMovieCardInfo(stat.movie_key))

        return returned_list
    
    # get top 10 weekly movies
    @staticmethod
    def getTopWeekly():
        movie_stats = data.MovieStatistics.objects.all()
        movie_stat_list = []
        for stat in movie_stats:
            movie_stat_list.append(stat)

        movie_stat_list.sort(key=lambda x: x.views_daily, reverse=True)
        movie_stat_list = movie_stat_list[:10]

        returned_list = []
        for stat in movie_stat_list:
            returned_list.append(MovieListing.generateMovieCardInfo(stat.movie_key))

        return returned_list
    
    # get top 10 monthly movies
    @staticmethod
    def getTopMonthly():
        movie_stats = data.MovieStatistics.objects.all()
        movie_stat_list = []
        for stat in movie_stats:
            movie_stat_list.append(stat)

        movie_stat_list.sort(key=lambda x: x.views_daily, reverse=True)
        movie_stat_list = movie_stat_list[:10]

        returned_list = []
        for stat in movie_stat_list:
            returned_list.append(MovieListing.generateMovieCardInfo(stat.movie_key))

        return returned_list

    # get top 10 annual movies
    @staticmethod
    def getTopAnnually():
        movie_stats = data.MovieStatistics.objects.all()
        movie_stat_list = []
        for stat in movie_stats:
            movie_stat_list.append(stat)

        movie_stat_list.sort(key=lambda x: x.views_daily, reverse=True)
        movie_stat_list = movie_stat_list[:10]

        returned_list = []
        for stat in movie_stat_list:
            returned_list.append(MovieListing.generateMovieCardInfo(stat.movie_key))

        return returned_list
    
    # take a list of movies and randomize it into a list of 20 elements
    @staticmethod
    def randomizeMovies(movies):
        movie_list = []
        for movie in movies:
            movie_list.append(movie)

        random.shuffle(movie_list)
        movie_list[:20]

        returned_list = []
        for movie in movie_list:
            returned_list.append(MovieListing.generateMovieCardInfo(movie))

        return returned_list
    
    # get random list of 20 movies
    @staticmethod
    def getRandomMovies():
        movies = data.Movie.objects.all()

        return MovieListing.randomizeMovies(movies)
    
    # get 20 movies restricted by a certain age rating
    @staticmethod
    def getMoviesRestrictedByAge(age_restriction):
        movies = data.Movie.objects.filter(age_restriction__lte=age_restriction)
            
        return MovieListing.randomizeMovies(movies)
    
    # get 20 movies of a certain age rating
    @staticmethod
    def getMoviesByAgeRestriction(age_restriction):
        movies = data.Movie.objects.filter(age_restriction__exact=age_restriction)
            
        return MovieListing.randomizeMovies(movies)
    
    # get 20 movies rated G or PG
    @staticmethod
    def getMoviesForKids():
        return MovieListing.getMoviesRestrictedByAge(2)
    
    # get 20 movies rated PG-13
    @staticmethod
    def getMoviesForTeens():
        return MovieListing.getMoviesByAgeRestriction(3)
    
    # get 20 movies rated R
    @staticmethod
    def getMoviesForAdults():
        return MovieListing.getMoviesByAgeRestriction(4)

