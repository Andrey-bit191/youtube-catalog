import requests
import json
import re

CHANNEL_ID = "UCdODFw-zhvUGCgc3QsnAag"

playlist_id = "UU" + CHANNEL_ID[2:]

url = f"https://www.youtube.com/playlist?list={playlist_id}"

html = requests.get(url).text

video_ids = re.findall(r"watch\\?v=(.{11})", html)

unique_ids = list(dict.fromkeys(video_ids))

videos = []

for vid in unique_ids:
    videos.append({
        "videoId": vid,
        "title": ""
    })

with open("videos.json","w") as f:
    json.dump(videos,f,indent=2)
