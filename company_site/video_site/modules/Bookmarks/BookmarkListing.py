from ..MovieData import MovieDataFunctions as mdf
from .. import MovieCardFormatting as mcf
from . import BookmarkFunctions as bf

class BookmarkListing:

    # Instantiates user age restriction and bookmarks
    def __init__(self, age_restriction, user_id):
        # This initializes the age_restriction to the value passed in or 4 by default
        self.age_restriction = age_restriction
        self.bookmarks = bf.getBookmarkEntriesByUser(user_id)


    # Generates all of the data needed for a movie card
    def __generateBookmarkMovieCardInfo(self, movie):
        # Create the String for how the age restriction should be displayed
        restriction_formatted = mcf.returnAgeRatingCardFormatted(movie.age_restriction)

        # Create the String for how the movie duration should be displayed
        duration_formatted = mcf.returnMovieDurationCardFormatted(movie.duration_seconds)

        # Create the Strong for how the genres should be displayed
        genres = mdf.getMovieGenreEntryByMovie(movie.movie_id)
        genres_formatted = mcf.returnGenresCardFormatted(genres)

        # Determine whether the bookmark icon is activated or not
        isBookmarked = bf.isMovieBookmarked(movie.movie_id, self.bookmarks)

        return [movie, restriction_formatted, duration_formatted, genres_formatted, isBookmarked]


    # get a list of all movies bookmarked by a user, and filtered by age restriction
    def getBookmarkedMovies(self):
        returned_list = []
        for movie in self.bookmarks:
            if self.age_restriction >= movie.movie_key.age_restriction:
                returned_list.append(self.__generateBookmarkMovieCardInfo(movie.movie_key))

        return ["Bookmarks", returned_list]