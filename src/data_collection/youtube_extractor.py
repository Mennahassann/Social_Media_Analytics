import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

def fetch_youtube_data(max_results=50):

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": CHANNEL_ID,
        "maxResults": max_results,
        "order": "date",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching YouTube videos: {response.text}")

    videos = response.json().get("items", [])
    video_data = []

    for v in videos:
        if v["id"]["kind"] == "youtube#video":
            video_id = v["id"].get("videoId")
            snippet = v["snippet"]

            stats_url = "https://www.googleapis.com/youtube/v3/videos"
            stats_params = {
                "part": "statistics", 
                "id": video_id,
                "key": API_KEY
                }
            stats_res = requests.get(stats_url, params=stats_params)
            stats = stats_res.json().get("items", [{}])[0].get("statistics", {})

            video_data.append({
                "id": video_id,
                "text": snippet.get("title", ""),
                "likes": stats.get("likeCount", 0),
                "comments": stats.get("commentCount", 0),
                "shares": stats.get("favoriteCount", 0), 
                "post_datetime": snippet.get("publishedAt"),
                "platform": "YouTube",
                "author_id": snippet.get("channelId", ""),
                "description": snippet.get("description", "")
            })

    return pd.DataFrame(video_data)


if __name__ == "__main__":
    df = fetch_youtube_data()
    print(df.head())
