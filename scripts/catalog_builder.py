import json
import subprocess
import os
import re

CHANNEL = "https://www.youtube.com/@PulseSignalOfficial/videos"

CATEGORIES = [
 "Master",
 "Remaster",
 "Live",
 "Jungle",
 "Club",
 "Dance",
 "Piano"
]

PAGE_SIZE = 20

print("Scanning channel...")

# получаем список видео
process = subprocess.run(
 [
  "yt-dlp",
  "--flat-playlist",
  "--dump-json",
  CHANNEL
 ],
 capture_output=True,
 text=True
)

lines = process.stdout.strip().split("\n")

videos = []

for line in lines:

 if not line.strip():
  continue

 try:
  data = json.loads(line)
  videos.append(data)
 except:
  continue

catalog = []
categories = {c.lower(): [] for c in CATEGORIES}

for v in videos:

 video_id = v.get("id")
 title = v.get("title","")

 if not video_id:
  continue

 video_categories = []

 for cat in CATEGORIES:

  pattern = r"\(" + cat + r"\)"
  if re.search(pattern,title,re.IGNORECASE):

   video_categories.append(cat.lower())
   categories[cat.lower()].append(video_id)

 if video_categories:

  catalog.append({
   "
