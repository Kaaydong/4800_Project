import random

from ..MovieData import MovieDataFunctions as mdf
from ..WatchHistory import WatchHistoryFunctions as whf
from .MovieListingFunctions import MovieListingFunctions

class MovieListing:
    def __init__(self, age_restriction = 4, user_id = -1):
        # This initializes the age_restriction to the value passed in or 4 by default
        self.age_restriction = age_restriction
        self.user_id = user_id
        
        self.mf = MovieListingFunctions(age_restriction, user_id)

    # Return a list of all movie lists to be rendered
    def returnListOfMovieLists(self):
        generated_movie_lists = []

        if self.user_id != -1:
            generated_movie_lists.append(self.getUserRecommended())
        else:
            generated_movie_lists.append(self.getRandomMovies())

        generated_movie_lists.append(self.getTopDaily())
        generated_movie_lists.append(self.getTopWeekly())
        generated_movie_lists.append(self.getTopAnnually())
        generated_movie_lists.append(self.getMoviesForKids())

        if self.user_id != -1:
            if self.age_restriction >= 3:
                generated_movie_lists.append(self.getMoviesForTeens())
            if self.age_restriction >= 4:
                generated_movie_lists.append(self.getMoviesForAdults())
            
        else:
            generated_movie_lists.append(self.getMoviesForTeens())
            generated_movie_lists.append(self.getMoviesForAdults())

        return generated_movie_lists


    # get random list of 20 movies
    def getRandomMovies(self):
        movies = mdf.getMoviesLessEqualAgeRestriction(self.age_restriction)

        return ["Movies We Recommend", self.mf.randomizeMovies(movies)]
    

    # get 20 movies recommended to the user
    def getUserRecommended(self):
        watched_movies = whf.getWatchEntryByUserAndAgeRestriction(self.user_id, self.age_restriction)

        # get a list of all genres
        all_genres = mdf.getAllGenres()
        genre_list = []
        for genre in all_genres:
            genre_list.append([genre, 0])

        # count how many movies of each genre the user watched
        for movie in watched_movies:
            movie_genres = mdf.getGenreEntriesOfMovie(movie.movie_key.movie_id)

            for i in range(0, len(genre_list)):
                for g in movie_genres:
                    if genre_list[i][0].genre == g.genre_key.genre:
                        genre_list[i][1] += 1
                        break

        # Sort genre_list from highest to lowest based on genre watch quantity
        genre_list.sort(key=lambda x: x[1], reverse=True)

        # Get movies, with most watched genres prioritized
        id_list = []
        return_list = []
        for g in genre_list:
            movies = mdf.getGenreEntriesByGenreAndAgeRestriction(g[0].genre_id, self.age_restriction)
            for m in movies:
                if not m.movie_key.movie_id in id_list:
                    id_list.append(m.movie_key.movie_id)
                    return_list.append(self.mf.generateMovieCardInfo(m.movie_key))

                if len(return_list) == 20:
                    break
            
            if len(return_list) == 20:
                    break
            
        random.shuffle(return_list)

        return ["Recommended For You", return_list]
    

    # get top 10 daily movies
    def getTopDaily(self):
        movie_stat_list = self.mf.generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_daily, reverse=True)

        return ["Trending Today", self.mf.convertStatsMovieListToReturnList(movie_stat_list)]
    

    # get top 10 weekly movies
    def getTopWeekly(self):
        movie_stat_list = self.mf.generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_weekly, reverse=True)

        return ["Hits This Week", self.mf.convertStatsMovieListToReturnList(movie_stat_list)]
    

    # get top 10 monthly movies
    def getTopMonthly(self):
        movie_stat_list = self.mf.generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_monthly, reverse=True)

        return ["Popular This Month", self.mf.convertStatsMovieListToReturnList(movie_stat_list)]


    # get top 10 annual movies
    def getTopAnnually(self):
        movie_stat_list = self.mf.generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_annually, reverse=True)

        return ["Big This Year", self.mf.convertStatsMovieListToReturnList(movie_stat_list)]
    

    # get 20 movies rated G or PG, assuming age restriction allows for it
    def getMoviesForKids(self):
        if self.age_restriction == 1:
            return ["For Kids", self.mf.getMoviesRestrictedByAge(1)]
        else:
            return ["For Kids", self.mf.getMoviesRestrictedByAge(2)]
    

    # get 20 movies rated PG-13
    def getMoviesForTeens(self):
        return ["For Teens", self.mf.getMoviesByAgeRestriction(3)]
    

    # get 20 movies rated R
    def getMoviesForAdults(self):
        return ["For Adults", self.mf.getMoviesByAgeRestriction(4)]

    # Get Movie by ID
    def getMovieById(self, movie_id):
        return self.mf.generateMovieCardInfo(mdf.getMovieById(movie_id, self.age_restriction))
        