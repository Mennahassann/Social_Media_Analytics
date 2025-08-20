import requests
import json

def get_youtube_posts(api_key, channel_handle):
    # Get channel ID first
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={channel_handle}&key={api_key}"
    data = requests.get(url).json()
    channel_id = data["items"][0]["id"]["channelId"]

    # Get videos
    url_videos = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=10&order=date&type=video&key={api_key}"
    videos = requests.get(url_videos).json()

    posts = []
    for v in videos["items"]:
        posts.append({
            "platform": "YouTube",
            "author_id": channel_id,
            "post_id": v["id"]["videoId"],
            "content": v["snippet"]["title"],
            "created_time": v["snippet"]["publishedAt"],
            "likes": None,
            "comments": None,
            "shares": None
        })
    return posts
def get_facebook_posts(page_id, access_token):
    url = f"https://graph.facebook.com/v21.0/{page_id}/posts"
    params = {
        "fields": "message,created_time,shares,likes.summary(true),comments.summary(true)",
        "limit": 10,
        "access_token": access_token
    }
    data = requests.get(url, params=params).json()
    posts = []
    for post in data.get("data", []):
        posts.append({
            "platform": "Facebook",
            "author_id": page_id,
            "post_id": post.get("id"),
            "content": post.get("message", ""),
            "created_time": post.get("created_time"),
            "likes": post.get("likes", {}).get("summary", {}).get("total_count", 0),
            "comments": post.get("comments", {}).get("summary", {}).get("total_count", 0),
            "shares": post.get("shares", {}).get("count", 0)
        })
    return posts
