# fetch_metrics.py

import requests
import pandas as pd

# Replace this with your actual access token
ACCESS_TOKEN = 'your_access_token_here'

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Step 1: Get list of uploaded videos
def get_video_list():
    url = "https://open.tiktokapis.com/v2/video/list/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to get video list:", response.text)
        return []

    videos = response.json().get("data", {}).get("videos", [])
    return [video["video_id"] for video in videos]

# Step 2: Get metrics for each video
def get_video_metrics(video_id):
    url = f"https://open.tiktokapis.com/v2/video/data/?video_ids={video_id}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to get metrics for {video_id}:", response.text)
        return None

    data = response.json().get("data", {}).get("videos", [])[0]
    return {
        "video_id": video_id,
        "views": data.get("play_count"),
        "likes": data.get("like_count"),
        "comments": data.get("comment_count"),
        "shares": data.get("share_count"),
    }

# Step 3: Combine into a DataFrame and save
def main():
    video_ids = get_video_list()
    if not video_ids:
        print("No videos found.")
        return

    metrics = []
    for vid in video_ids:
        result = get_video_metrics(vid)
        if result:
            metrics.append(result)

    df = pd.DataFrame(metrics)
    df.to_csv("data/metrics.csv", index=False)
    print("Metrics saved to data/metrics.csv")

if __name__ == "__main__":
    main()
