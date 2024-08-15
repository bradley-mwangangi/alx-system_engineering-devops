import requests
from collections import Counter

def count_words(subreddit, word_list, hot_list=[], after=None):
    """Recursively queries the Reddit API, counts and prints sorted keyword occurrences."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'custom_user_agent/0.1'}
    params = {'limit': 100, 'after': after}
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )
        if response.status_code == 200:
            data = response.json().get("data", {})
            posts = data.get("children", [])
            after = data.get("after", None)
            
            # Collect titles from the current page
            for post in posts:
                title = post.get("data", {}).get("title", "").lower()
                hot_list.append(title)
            
            # Continue to the next page if there is one
            if after is not None:
                return count_words(subreddit, word_list, hot_list, after)
            
            # Count keyword occurrences across all titles
            word_count = Counter()
            for title in hot_list:
                words = title.split()
                for word in word_list:
                    word_count[word.lower()] += words.count(word.lower())
            
            # Filter out words with 0 occurrences
            word_count = {
                word: count for word, count in word_count.items() if count > 0
            }
            
            # Sort the results first by count (descending), then alphabetically (ascending)
            sorted_word_count = sorted(
                word_count.items(),
                key=lambda item: (-item[1], item[0])
            )
            
            # Print the results
            if sorted_word_count:
                for word, count in sorted_word_count:
                    print(f"{word}: {count}")
            else:
                print("")  # Explicitly print nothing for empty results
        else:
            print("")  # Explicitly print nothing for invalid subreddit
    except requests.RequestException:
        print("")  # Explicitly print nothing on request failure
