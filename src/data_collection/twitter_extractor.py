import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
USERNAME = os.getenv("TWITTER_USERNAME")

def get_headers():
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}"
        }

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code == 429:
        print("Rate limit exceeded. Waiting 30 seconds...")
        time.sleep(30)
        return get_user_id(username)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching user ID: {response.text}")
    
    return response.json()["data"]["id"]

def fetch_tweets(username=USERNAME, max_results=5, retries=5):
    user_id = get_user_id(username)
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    
    params = {"max_results": max_results, 
            "tweet.fields": "public_metrics,"
            "created_at,"
            "author_id"
            }

    for i in range(retries):
        response = requests.get(url, headers=get_headers(), params=params)
        if response.status_code == 200:
            tweets = response.json().get("data", [])
            df = pd.DataFrame([
                {
                    "id": t.get("id", ""),
                    "text": t.get("text", ""),
                    "created_at": t.get("created_at", ""),
                    "likes": t.get("public_metrics", {}).get("like_count", 0),
                    "shares": t.get("public_metrics", {}).get("retweet_count", 0),
                    "comments": t.get("public_metrics", {}).get("reply_count", 0),
                    "author_id": t.get("author_id", user_id)
                } for t in tweets
            ])
            return df

        elif response.status_code == 429:
            wait_time = (i + 1) * 30
            print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"Error fetching tweets: {response.text}")

    raise Exception("Failed to fetch tweets after multiple retries.")

if __name__ == "__main__":
    df = fetch_tweets()
    print(df.head())
