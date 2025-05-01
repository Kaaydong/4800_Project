from ...models import BookmarkEntry
from ..MovieData import MovieDataFunctions as mdf

# Return all bookmark entries belonging to a user
def getBookmarkEntriesByUser(user_id):
    return BookmarkEntry.objects.filter(user_key=user_id)

# Return whether the movie is bookmarked or not
def isMovieBookmarked(movie_id, bookmarks):
    isBookmarked = False
    try:
        bookmarks.get(movie_key=movie_id)
        isBookmarked = True
    except:
        isBookmarked = False

    return isBookmarked

# Creates a new bookmark entry given a user id and movie id
def createBookmarkEntry(user_id, movie_id):
    bookmark = BookmarkEntry(user_key=user_id, movie_key=mdf.getMovieById(movie_id))
    bookmark.save()

# Delete BookmarkEntry by user key and movie key
def deleteBookmarkEntry(user_id, movie_id):
    user_bookmark = BookmarkEntry.objects.get(user_key=user_id, movie_key=movie_id)
    user_bookmark.delete()