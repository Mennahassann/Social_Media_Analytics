import pandas as pd
from data_collection.twitter_extractor import fetch_tweets
from data_collection.youtube_extractor import fetch_youtube_data
from data_processing.transformer import clean_and_transform
from data_processing.cleantext import clean_text

def run_pipeline():

    #Extract
    tw_data = fetch_tweets(username="NaguibSawiris", max_results=10)  
    yt_data = fetch_youtube_data( max_results=10) 

    tw_data["text"] = tw_data["text"].apply(clean_text)
    yt_data["text"] = yt_data["text"].apply(clean_text)

    #Normalize
    tw_data = clean_and_transform(tw_data, platform="Twitter")
    yt_data = clean_and_transform(yt_data, platform="YouTube")

    #Combine
    data = [tw_data, yt_data]
    data_unified = pd.concat(data, ignore_index=True)
    data_unified = data_unified.sort_values("created_at", ascending=False)
    
    #load
    data_unified.to_csv("unified_Schema.csv", index=False, encoding="utf-8-sig")
    print("Unified dataset created, Rows:", len(data_unified))

if __name__ == "__main__":
    run_pipeline()
