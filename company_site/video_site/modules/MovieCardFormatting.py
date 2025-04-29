# Return the age rating of a movie in String form for a movie card
def returnAgeRatingCardFormatted(restriction):
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

    return restriction_formatted

# Return the duration of a movie in String form for a movie card
def returnMovieDurationCardFormatted(duration):
    hours = duration // 3600
    if hours > 0:
        duration_formatted = str(duration // 3600) + "h "
        duration_formatted += str(duration % 3600 // 60) + "m"
    else:
        duration_formatted = str(duration // 60) + "m "
        duration_formatted += str(duration % 60) + "s"

    return duration_formatted

# Return the 3 or less genres of a movie in String form for a movie card
def returnGenresCardFormatted(genres):
    genres_formatted = ""
    genres = genres[:3]
    for i in range(0, len(genres)):
        genres_formatted += genres[i].genre_key.genre
        if i < len(genres) - 1:
            genres_formatted += ", " 
    
    return genres_formatted