from ...models import Movie, MovieActorEntry, MovieGenreEntry

def getMovieGenreEntryByMovie(movie_id):
    return MovieGenreEntry.objects.filter(movie_key=movie_id)