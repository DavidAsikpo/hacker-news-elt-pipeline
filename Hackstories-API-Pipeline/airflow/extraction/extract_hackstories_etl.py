import requests
import time
import json
import pandas
import sys 
import io
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



# Get the output name from the command line
if len(sys.argv) < 2:
    print("Usage: python fetch_hackstories.py <output_name>")
    sys.exit(1)

output_name = sys.argv[1]
FILENAME = f"{output_name}.csv"

# Calculate the timestamp for 1000 days ago
thousand_days_ago = int(time.time()) - (1000 * 24 * 60 * 60)

# Define the API endpoint and parameters
url = "https://hn.algolia.com/api/v1/search"



def get_session_with_retries():
    """Create a requests session with retry logic"""
    try: 
        session = requests.Session()
        retries = Retry(total=5, connect=5, read = 5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    except Exception as e:
        print(f"Error creating session: {e}")
        return None

def fetch_hackstories():
    
    current_page = 0
    max_pages = 1

    posts = []

    session = get_session_with_retries()
    if session is None:
        print("Failed to create a session. Exiting.")
        sys.exit(1)

    while current_page < max_pages:
        params = {
            "query": "AI",
            "tags": "story",
            "numericFilters": f"created_at_i>{thousand_days_ago}",
            "hitsPerPage": 100,
            "page": current_page
        }

        # Make the request
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling session: {e}")
            sys.exit(1)
        max_pages = data.get("nbPages", 1)  # Update max_pages based on the response

        for hit in data.get("hits", []):
            if hit.get("points", 0) < 300:
                continue 
            if hit.get("points") is None or hit.get("num_comments") is None:
                continue
            if not hit.get("author") or not hit.get("title"):
                continue
            # Skip posts with less than 300 points
            post = {    "id": hit.get("objectID"),
                        "title": hit.get("title"),
                        "url": hit.get("url"),
                        "author": hit.get("author"),
                        "created_at": hit.get("created_at"),
                        "points": hit.get("points"),
                        "num_comments": hit.get("num_comments")
                    }
            posts.append(post) 

        current_page += 1

        time.sleep(1)  # Sleep for 1 second to avoid hitting the API too quickly

    posts_df = pandas.DataFrame(posts)
    
    print(f"Processed {len(posts)} posts successfully!")
    
    posts_df.to_csv(f"/tmp/{FILENAME}", index=False)

    print(f"file saved successfully!")



if __name__ == "__main__":
    #run pipeline
    fetch_hackstories()






