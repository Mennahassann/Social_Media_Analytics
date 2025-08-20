import pandas as pd

def load_unified_data(file="unified_Schema.csv"):
    df = pd.read_csv(file)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
    return df

def compute_daily_metrics(df):
    daily_engagement = (
        df.groupby([df["created_at"].dt.date, "platform"])
            [["likes", "comments", "shares", "engagement_score"]]
            .sum()
            .reset_index()
            .rename(columns={"created_at": "date"})
    )
    daily_engagement.to_csv("daily_engagement_metrics.csv", index=False, encoding="utf-8-sig")
    print("Daily engagement metrics saved.")
    return daily_engagement

def compute_top_posts(df, top_n = 5, top_n_per_platform = 3):
    top_5 = df.sort_values("engagement_score", ascending=False).head(top_n)
    top_per_platform = df.sort_values("engagement_score", ascending=False).groupby("platform").head(top_n_per_platform)
    
    top_posts = pd.concat([top_5, top_per_platform]).drop_duplicates().reset_index(drop=True)
    top_posts.to_csv("top_posts.csv", index=False, encoding="utf-8-sig")
    print("Top posts saved.")
    return top_posts


def run_analyzer():
    df = load_unified_data()
    
    print("\n--- Computing Daily Engagement Metrics ---")
    daily_metrics = compute_daily_metrics(df)
    print(daily_metrics.head(10))
    
    print("\n--- Computing Top Posts ---")
    top_posts = compute_top_posts(df)
    print(top_posts[["platform", "text", "engagement_score"]].head(10))

if __name__ == "__main__":
    run_analyzer()
