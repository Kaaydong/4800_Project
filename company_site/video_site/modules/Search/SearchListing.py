from ..MovieData import MovieDataFunctions as mdf
from ..Movies.MoviesFunctions import MoviesFunctions
from . import SearchFunctions as sf

class SearchListing:
    def __init__(self, age_restriction = 4, user_id = -1):
        # This initializes the age_restriction to the value passed in or 4 by default
        self.age_restriction = age_restriction
        self.movie_stats = mdf.getAllMovieStats()

        self.user_id = user_id
        self.mf = MoviesFunctions(age_restriction, user_id)

    # Get Movie by a String query and Genre filter
    def getMoviesByQuery(self, query, filter):
        
        # If query is empty, get movies purely by genre filter, if filter even exists
        if query == None or query == "":
            # Filter is empty
            if filter == None or filter == -1:
                results_filtered_genre = mdf.getAllMovies()

            # Filter genre exists
            else:
                movies_from_genre = mdf.getGenreEntriesByGenre(filter)

                results_filtered_genre = []
                for movie in movies_from_genre:
                    results_filtered_genre.append(movie.movie_key)
        
        # Query Exists, now do a string match
        else:
            # Make query all lowercase
            query = query.lower()

            # String match with movie title
            movie_names = mdf.getMovieValueList('title')
            movie_matches = sf.getCloseMatches(query, movie_names, 0.8)
            movie_results = mdf.getAllMoviesFromTitles(movie_matches)

            # String match with actor's names
            actor_first_names = mdf.getActorValueList('first_name')
            actor_middle_names = mdf.getActorValueList('middle_name')
            actor_last_names = mdf.getActorValueList('last_name')
            
            # Have a first + last name string to have a better match case
            actor_first_last_names = []
            for f, l in zip(actor_first_names, actor_last_names):
                actor_first_last_names.append(f + " " + l)

            first_name_matches = sf.getCloseMatches(query, actor_first_names, 0.8)
            middle_name_matches = sf.getCloseMatches(query, actor_middle_names, 0.8)
            last_name_matches = sf.getCloseMatches(query, actor_last_names, 0.8)
            first_last_name_matches = sf.getCloseMatches(query, actor_first_last_names, 0.85)

            # Just take the first name of the first and last name pair since that is all that is needed
            for name in first_last_name_matches:
                first_name_matches.append(name[:name.find(' ')])

            first_name_results = mdf.getMovieKeysByListOfFirstNames(first_name_matches)
            middle_name_results = mdf.getMovieKeysByListOfMiddleNames(middle_name_matches)
            last_name_results = mdf.getMovieKeysByListOfLastNames(last_name_matches)

            key_list = set(first_name_results).union(set(middle_name_results)).union(set(last_name_results))
            name_results = mdf.getAllMoviesFromMovieKeys(key_list)

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
                        q = mdf.getGenreEntriesByMovieAndGenre(result.movie_id, filter)
                        results_filtered_genre.append(q.movie_key)
                    except:
                        results_filtered_genre
                
        return_list = []
        for result in results_filtered_genre:
            if result.age_restriction <= self.age_restriction:
                return_list.append(self.mf.generateMovieCardInfo(result))

        return ["", return_list]
