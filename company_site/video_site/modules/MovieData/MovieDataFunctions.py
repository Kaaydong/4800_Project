from ...models import Movie, Actor, Genre, MovieGenreEntry, MovieActorEntry, MovieStatistics

# Return all movies
def getAllMovies():
    return Movie.objects.all() 

def getAllMoviesFromMovieKeys(key_list):
    return Movie.objects.filter(movie_id__in=key_list)

# Get all movies from a list of movie_titles
def getAllMoviesFromTitles(title_list):
    return Movie.objects.filter(title__in=title_list)

# Returns a movie object by movie_id and if user age restriction allows
def getMovieById(movie_id, age_restriction=4):
    try:
        # Query to retrieve the movie by its movie_id using the correct model
        movie = Movie.objects.get(movie_id=movie_id)

        # Now filter the movie by the user's age restriction
        if movie.age_restriction <= age_restriction:
            # Return the movie if it matches the age restriction
            return movie
        else:
            # If the movie doesn't match the user's age restriction, return None
            return None
    except Movie.DoesNotExist:
        # If the movie with the given ID does not exist, return None
        return None

# Return movies with a specific age restriction
def getMoviesEqualAgeRestriction(age_restriction):
    return Movie.objects.filter(age_restriction__exact=age_restriction)

# Return movies less than or equal to an age restriction
def getMoviesLessEqualAgeRestriction(age_restriction):
    return Movie.objects.filter(age_restriction__lte=age_restriction)

# Return all movie actor entries for a movie
def getAllMovieActorEntriesOfMovie(movie_id):
    return MovieActorEntry.objects.filter(movie_key=movie_id)

# Return a list of movie keys given an list of actors first names
def getMovieKeysByListOfFirstNames(first_name_list):
    return MovieActorEntry.objects.filter(actor_key__first_name__in=first_name_list).values_list('movie_key', flat=True)

# Return a list of movie keys given an list of actors middle names
def getMovieKeysByListOfMiddleNames(middle_name_list):
    return MovieActorEntry.objects.filter(actor_key__middle_name__in=middle_name_list).values_list('movie_key', flat=True)

# Return a list of movie keys given an list of actors last names
def getMovieKeysByListOfLastNames(last_name_list):
    return MovieActorEntry.objects.filter(actor_key__last_name__in=last_name_list).values_list('movie_key', flat=True)

# Return list of a specific attribute of all movies
def getMovieValueList(attribute):
    return Movie.objects.values_list(attribute, flat=True)

# Return list of a specific attribute of all actors
def getActorValueList(attribute):
    return Actor.objects.values_list(attribute, flat=True)

# Get all genre objects
def getAllGenres():
    return Genre.objects.all()

# Get all genre entries of a movie by movie_id
def getGenreEntriesOfMovie(movie_id):
    return MovieGenreEntry.objects.filter(movie_key=movie_id)

# Get all genre entries for a specific genre
def getGenreEntriesByGenre(genre_id):
    return MovieGenreEntry.objects.filter(genre_key=genre_id)

# Get genre entry of a specific movie and genre
def getGenreEntriesByMovieAndGenre(movie_id, genre_key):
    return MovieGenreEntry.objects.get(movie_key=movie_id, genre_key=genre_key)

# Get all genre entries of a movie by movie_id, filtered by user age restriction
def getGenreEntriesByGenreAndAgeRestriction(genre_id, age_restriction):
    return MovieGenreEntry.objects.filter(genre_key=genre_id, movie_key__age_restriction__lte=age_restriction)

# Get all Movie Stat objects
def getAllMovieStats():
    return MovieStatistics.objects.all()