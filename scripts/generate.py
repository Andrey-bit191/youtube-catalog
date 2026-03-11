import requests
import xml.etree.ElementTree as ET
import json

url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCyIYw0p9xI9qFv4g3uYt7sA"

response = requests.get(url)

root = ET.fromstring(response.content)

videos = []

for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):

    video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
    title = entry.find("{http://www.w3.org/2005/Atom}title").text

    videos.append({
        "videoId": video_id,
        "title": title,
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        "url": f"https://youtube.com/watch?v={video_id}"
    })

with open("videos.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=2)

print("Videos found:", len(videos))
