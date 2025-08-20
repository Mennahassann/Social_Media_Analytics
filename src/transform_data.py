import pandas as pd

all_posts = get_youtube_posts(youtube_key, youtube_channel) + get_facebook_posts(facebook_page_id, facebook_token)
df = pd.DataFrame(all_posts)
df["engagement_score"] = df[["likes","comments","shares"]].fillna(0).sum(axis=1)
