from difflib import get_close_matches

# Get list of movies that match a specific query parameter to a certain matching extent
def getCloseMatches(query, match_list, cutoff):
    match_list = list(match_list)
    lowercase_list = [item.lower() for item in match_list]

    matched_list = get_close_matches(query, lowercase_list, n=20, cutoff=cutoff)
    
    return_list = []
    for item in matched_list:
        for name in match_list:
            if item == name.lower():
                return_list.append(name)
                break
    
    return return_list
