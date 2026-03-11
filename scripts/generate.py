import requests
import xml.etree.ElementTree as ET
import json

URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UC0lG6IH2cQd5V7Hn1j6f3hQ"

headers = {
    "User-Agent": "Mozilla/5.0"
}

videos = []

try:
    r = requests.get(URL, headers=headers, timeout=20)

    if r.status_code == 200:
        root = ET.fromstring(r.content)

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
            title = entry.find("{http://www.w3.org/2005/Atom}title").text

            videos.append({
                "videoId": video_id,
                "title": title,
                "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                "url": f"https://youtube.com/watch?v={video_id}"
            })

except Exception as e:
    print("Error:", e)

# Файл создаётся ВСЕГДА
with open("videos.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=2, ensure_ascii=False)

print("Videos:", len(videos))
