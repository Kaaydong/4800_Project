import random
from .. import MovieCardFormatting as mcf
from ..Bookmarks import BookmarkFunctions as bf
from ..MovieData import MovieDataFunctions as mdf

class MoviesFunctions:
    def __init__(self, age_restriction, user_id):
        # This initializes the age_restriction to the value passed in or 4 by default
        self.age_restriction = age_restriction
        self.movie_stats = mdf.getAllMovieStats()

        self.user_id = user_id
        if user_id != -1:
            self.bookmarks = bf.getBookmarkEntriesByUser(user_id)

    # Queries for every movie's stats and turns it into a list
    def generateStatisticsList(self):
        movie_stat_list = []
        for stat in self.movie_stats:
            movie_stat_list.append(stat)

        return movie_stat_list


    # returns a movie as a tuple, with all of its required data
    # FORMAT = [movie, duration_formatted, restriction_formatted, genres_formatted, isMovieBookmarked]
    def generateMovieCardInfo(self, movie):
        duration = movie.duration_seconds
        genres = mdf.getGenreEntriesOfMovie(movie.movie_id)

        # Create the String for how the age restriction should be displayed
        restriction_formatted = mcf.returnAgeRatingCardFormatted(movie.age_restriction)

        # Create the String for how the movie duration should be displayed
        duration_formatted = mcf.returnMovieDurationCardFormatted(duration)

        # Create the Strong for how the genres should be displayed
        genres_formatted = mcf.returnGenresCardFormatted(genres)

        # Determine whether the bookmark icon is activated or not
        isBookmarked = False
        if self.user_id != -1:
            try:
                self.bookmarks.get(movie_key=movie.movie_id)
                isBookmarked = True
            except:
                isBookmarked = False

        return [movie, restriction_formatted, duration_formatted, genres_formatted, isBookmarked]


    # Take a sorted statistics list and return 10 movies in the proper format
    def convertStatsMovieListToReturnList(self, movie_stat_list):
        new_movie_stat_list = []
        for stat in movie_stat_list:
            if self.age_restriction >= stat.movie_key.age_restriction:
                new_movie_stat_list.append(stat.movie_key)

        new_movie_stat_list = new_movie_stat_list[:10]

        returned_list = []
        for key in new_movie_stat_list:
            returned_list.append(self.generateMovieCardInfo(key))
        
        return returned_list


    # take a list of movies and randomize it into a list of 20 elements
    def randomizeMovies(self, movies):
        movie_list = []
        for movie in movies:
            movie_list.append(movie)

        random.shuffle(movie_list)
        movie_list[:20]

        returned_list = []
        for movie in movie_list:
            returned_list.append(self.generateMovieCardInfo(movie))

        return returned_list


    # get 20 movies restricted by a certain age rating
    def getMoviesRestrictedByAge(self, age_restriction):
        movies = mdf.getMoviesLessEqualAgeRestriction(age_restriction)
            
        return self.randomizeMovies(movies)


    # get 20 movies of a certain age rating
    def getMoviesByAgeRestriction(self, age_restriction):
        movies = mdf.getMoviesEqualAgeRestriction(age_restriction)
            
        return self.randomizeMovies(movies)