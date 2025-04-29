from ...models import BookmarkEntry

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