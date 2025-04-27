import random
from django.contrib.auth import get_user_model

from .. import models as data
from difflib import get_close_matches


class MovieListing:
    def __init__(self, age_restriction = 4, user_id = -1):
        # This initializes the age_restriction to the value passed in or 4 by default
        self.age_restriction = age_restriction
        self.movie_stats = data.MovieStatistics.objects.all()

        self.user_id = user_id
        if user_id != -1:
            self.bookmarks = data.BookmarkEntry.objects.filter(user_key=user_id)
        

    # returns a movie as a tuple, with all of its required data
    # FORMAT = [movie, duration_formatted, restriction_formatted, genres_formatted, isMovieBookmarked]
    def __generateMovieCardInfo(self, movie, isWatchEntry=False):
        duration = movie.duration_seconds
        restriction = movie.age_restriction
        genres = data.MovieGenreEntry.objects.filter(movie_key=movie.movie_id)

        # Create the String for how the age restriction should be displayed
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

        # Create the String for how the movie duration should be displayed
        duration_formatted = ""
        if not isWatchEntry:
            hours = duration // 3600
            if hours > 0:
                duration_formatted = str(duration // 3600) + "h "
                duration_formatted += str(duration % 3600 // 60) + "m"
            else:
                duration_formatted = str(duration // 60) + "m "
                duration_formatted += str(duration % 60) + "s"
        
        else:
            file_duration = movie.file_duration_seconds
            watch_timestamp = data.WatchEntry.objects.get(user_key=self.user_id, movie_key=movie.movie_id).watch_progress
            watch_timestamp = int(watch_timestamp * 100 // file_duration)

            if watch_timestamp >= 99:
                duration_formatted = [100, "completed"]
            else:
                duration_formatted = [watch_timestamp, str(watch_timestamp) + "%"]

        # Create the Strong for how the genres should be displayed
        genres_formatted = ""
        genres = genres[:3]
        for i in range(0, len(genres)):
            genres_formatted += genres[i].genre_key.genre
            if i < len(genres) - 1:
                genres_formatted += ", " 

        # Determine whether the bookmark icon is activated or not
        isBookmarked = False
        if self.user_id != -1:
            try:
                self.bookmarks.get(movie_key=movie.movie_id)
                isBookmarked = True
            except:
                isBookmarked = False

        return [movie, restriction_formatted, duration_formatted, genres_formatted, isBookmarked]



    # get 20 movies recommended to the user
    def getUserRecommended(self):
        watched_movies = data.WatchEntry.objects.filter(user_key=self.user_id, movie_key__age_restriction__lte=self.age_restriction)

        # get a list of all genres
        all_genres = data.Genre.objects.all()
        genre_list = []
        for genre in all_genres:
            genre_list.append([genre, 0])

        # count how many movies of each genre the user watched
        for movie in watched_movies:
            movie_genres = data.MovieGenreEntry.objects.filter(movie_key=movie.movie_key.movie_id)

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
            movies = data.MovieGenreEntry.objects.filter(genre_key=g[0].genre_id, movie_key__age_restriction__lte=self.age_restriction)
            for m in movies:
                if not m.movie_key.movie_id in id_list:
                    id_list.append(m.movie_key.movie_id)
                    return_list.append(self.__generateMovieCardInfo(m.movie_key))

                if len(return_list) == 20:
                    break
            
            if len(return_list) == 20:
                    break
            
        random.shuffle(return_list)

        return ["Recommended For You", return_list]
        

    # Queries for every movie's stats and turns it into a list
    def __generateStatisticsList(self):
        movie_stat_list = []
        for stat in self.movie_stats:
            movie_stat_list.append(stat)

        return movie_stat_list
    

    # Take a sorted statistics list and return 10 movies in the proper format
    def __convertStatsMovieListToReturnList(self, movie_stat_list):
        movie_stat_list = movie_stat_list[:10]

        returned_list = []
        for stat in movie_stat_list:
            returned_list.append(self.__generateMovieCardInfo(stat.movie_key))
        
        return returned_list


    # get top 10 daily movies
    def getTopDaily(self):
        movie_stat_list = self.__generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_daily, reverse=True)

        return ["Trending Today", self.__convertStatsMovieListToReturnList(movie_stat_list)]
    

    # get top 10 weekly movies
    def getTopWeekly(self):
        movie_stat_list = self.__generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_weekly, reverse=True)

        return ["Hits This Week", self.__convertStatsMovieListToReturnList(movie_stat_list)]
    

    # get top 10 monthly movies
    def getTopMonthly(self):
        movie_stat_list = self.__generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_monthly, reverse=True)

        return ["Popular This Month", self.__convertStatsMovieListToReturnList(movie_stat_list)]


    # get top 10 annual movies
    def getTopAnnually(self):
        movie_stat_list = self.__generateStatisticsList()
        movie_stat_list.sort(key=lambda x: x.views_annually, reverse=True)

        return ["Big This Year", self.__convertStatsMovieListToReturnList(movie_stat_list)]
    

    # take a list of movies and randomize it into a list of 20 elements
    def __randomizeMovies(self, movies):
        movie_list = []
        for movie in movies:
            movie_list.append(movie)

        random.shuffle(movie_list)
        movie_list[:20]

        returned_list = []
        for movie in movie_list:
            returned_list.append(self.__generateMovieCardInfo(movie))

        return returned_list
    

    # get random list of 20 movies
    def getRandomMovies(self):
        movies = data.Movie.objects.filter(age_restriction__lte=self.age_restriction)

        return ["Movies We Recommend", self.__randomizeMovies(movies)]
    

    # get 20 movies restricted by a certain age rating
    def __getMoviesRestrictedByAge(self, age_restriction):
        movies = data.Movie.objects.filter(age_restriction__lte=age_restriction) # YES THIS QUERY IS CORRECT 
            
        return self.__randomizeMovies(movies)
    

    # get 20 movies of a certain age rating
    def __getMoviesByAgeRestriction(self, age_restriction):
        movies = data.Movie.objects.filter(age_restriction__exact=age_restriction) # YES THIS QUERY IS ALSO CORRECT 
            
        return self.__randomizeMovies(movies)
    

    # get 20 movies rated G or PG
    def getMoviesForKids(self):
        return ["For Kids", self.__getMoviesRestrictedByAge(2)]
    

    # get 20 movies rated PG-13
    def getMoviesForTeens(self):
        return ["For Teens", self.__getMoviesByAgeRestriction(3)]
    

    # get 20 movies rated R
    def getMoviesForAdults(self):
        return ["For Adults", self.__getMoviesByAgeRestriction(4)]
    
    # get a list of all movies bookmarked by a user
    def getBookmarkedMovies(self):
        returned_list = []
        for movie in self.bookmarks:
            returned_list.append(self.__generateMovieCardInfo(movie.movie_key))

        return ["Bookmarks", returned_list]
    
    # get a list of all movies watched by a user
    def getWatchedMovies(self):
        returned_list = []

        watched_movies = data.WatchEntry.objects.filter(user_key=self.user_id)
        for movie in watched_movies:
            if movie.watch_progress >= 1:
                returned_list.append(self.__generateMovieCardInfo(movie.movie_key, True))

        return ["Watch History", returned_list]

    # Get Movie by ID
    def getMovieById(self, movie_id):
        try:
            # Query to retrieve the movie by its movie_id using the correct model
            movie = data.Movie.objects.get(movie_id=movie_id)

            # Now filter the movie by the user's age restriction
            if movie.age_restriction <= self.age_restriction:
                # Return the movie if it matches the age restriction
                return self.__generateMovieCardInfo(movie)
            else:
                # If the movie doesn't match the user's age restriction, return None
                return None
        except data.Movie.DoesNotExist:
            # If the movie with the given ID does not exist, return None
            return None
        

    # Get Movie by a String query and Genre filter
    def getMoviesByQuery(self, query, filter):
        
        # If query is empty, get movies purely by genre filter, if filter even exists
        if query == None or query == "":
            # Filter is empty
            if filter == None or filter == -1:
                results_filtered_genre = data.Movie.objects.all()

            # Filter genre exists
            else:
                movies_from_genre = data.MovieGenreEntry.objects.filter(genre_key=filter)

                results_filtered_genre = []
                for movie in movies_from_genre:
                    results_filtered_genre.append(movie.movie_key)
        
        # Query Exists, now do a string match
        else:
            # String match with movie title
            movie_names = data.Movie.objects.values_list('title', flat=True)
            movie_matches = get_close_matches(query, movie_names, n=15, cutoff=0.3)
            movie_results = data.Movie.objects.filter(title__in=movie_matches)

            # String match with actor's names
            actor_first_names = data.Actor.objects.values_list('first_name', flat=True)

            actor_middle_names = data.Actor.objects.values_list('middle_name', flat=True)
            actor_last_names = data.Actor.objects.values_list('last_name', flat=True)
            
                # Have a first + last name string to have a better match case
            actor_first_last_names = []
            for f, l in zip(actor_first_names, actor_last_names):
                actor_first_last_names.append(f + " " + l)

            first_name_matches = get_close_matches(query, actor_first_names, n=15, cutoff=0.56)
            middle_name_matches = get_close_matches(query, actor_middle_names, n=15, cutoff=0.76)
            last_name_matches = get_close_matches(query, actor_last_names, n=15, cutoff=0.56)
            first_last_name_matches = get_close_matches(query, actor_first_last_names, n=15, cutoff=0.85)

                # Just take the first name of the first and last name pair since that is all that is needed
            for name in first_last_name_matches:
                first_name_matches.append(name[:name.find(' ')])

            first_name_results = data.MovieActorEntry.objects.filter(actor_key__first_name__in=first_name_matches).values_list('movie_key', flat=True)
            middle_name_results = data.MovieActorEntry.objects.filter(actor_key__middle_name__in=middle_name_matches).values_list('movie_key', flat=True)
            last_name_results = data.MovieActorEntry.objects.filter(actor_key__last_name__in=last_name_matches).values_list('movie_key', flat=True)

            key_list = set(first_name_results).union(set(middle_name_results)).union(set(last_name_results))
            name_results = data.Movie.objects.filter(movie_id__in=key_list)

            # Final movie list
            movie_results = set(movie_results).union(set(name_results))

            # Filter is empty
            results_filtered_genre = []
            if filter == None or filter == -1:
                results_filtered_genre = list(movie_results)

            # Filter genre exists
            else:
                for result in movie_results:
                    try:
                        q = data.MovieGenreEntry.objects.get(movie_key=result.movie_id, genre_key=filter)
                        results_filtered_genre.append(q.movie_key)
                    except:
                        results_filtered_genre
                
        return_list = []
        for result in results_filtered_genre:
            return_list.append(self.__generateMovieCardInfo(result))

        return ["", return_list]
