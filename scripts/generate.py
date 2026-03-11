import requests
import json
import re

CHANNEL = "https://www.youtube.com/@PulseSignalOfficial/videos"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(CHANNEL, headers=headers).text

data = re.search(r"var ytInitialData = ({.*?});", html)

if not data:
    print("No data found")
    exit()

json_data = json.loads(data.group(1))

videos = []

items = json_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]["content"]["richGridRenderer"]["contents"]

for item in items:

    if "richItemRenderer" not in item:
        continue

    video = item["richItemRenderer"]["content"]["videoRenderer"]

    video_id = video["videoId"]
    title = video["title"]["runs"][0]["text"]

    videos.append({
        "videoId": video_id,
        "title": title,
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        "url": f"https://youtube.com/watch?v={video_id}"
    })

with open("videos.json", "w", encoding="utf8") as f:
    json.dump(videos, f, indent=2, ensure_ascii=False)

print("Videos:", len(videos))
