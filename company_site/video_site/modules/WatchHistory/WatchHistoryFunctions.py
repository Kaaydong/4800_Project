from ...models import WatchEntry

# Get a list of all watch entries for a user
def getWatchEntriesByUser(user_id):
    return WatchEntry.objects.filter(user_key=user_id)

# Get a specific watch entry of a movie for a user
def getWatchEntryByUserAndMovies(user_id, movie_id):
    return WatchEntry.objects.get(user_key=user_id, movie_key=movie_id)

# Get a list of watch entries for a user, filtered by age restriction
def getWatchEntryByUserAndAgeRestriction(user_id, age_restriction):
    return WatchEntry.objects.filter(user_key=user_id, movie_key__age_restriction__lte=age_restriction)

# Returns a list that contains the percentage of a movie watched
# - 1st element is the int representation
# - 2nd element is the string representation
def getWatchEntryTimestampFormatted(user_id, movie):
    file_duration = movie.file_duration_seconds
    watch_timestamp = getWatchEntryByUserAndMovies(user_id, movie.movie_id).watch_progress
    watch_timestamp = int(watch_timestamp * 100 // file_duration)

    if watch_timestamp >= 99:
        timestamp_formatted = [100, "completed"]
    else:
        timestamp_formatted = [watch_timestamp, str(watch_timestamp) + "%"]

    return timestamp_formatted


