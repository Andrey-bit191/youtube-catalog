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


def detect_category(title):

 result = []

 for cat in CATEGORIES:

  pattern = r"\(" + cat + r"\)"

  if re.search(pattern,title,re.IGNORECASE):
   result.append(cat.lower())

 return result


# PUBLIC VIDEOS

for v in videos:

 video_id = v.get("id")
 title = v.get("title","")

 if not video_id:
  continue

 cats = detect_category(title)

 if cats:

  catalog.append({
   "id": video_id,
   "title": title,
   "category": cats,
   "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
  })

  for c in cats:
   categories[c].append(video_id)


# PRIVATE VIDEOS

private_path = "catalog/private_videos.json"

if os.path.exists(private_path):

 with open(private_path) as f:
  private_videos = json.load(f)

 for v in private_videos:

  video_id = v["id"]
  title = v["title"]
  cats = v["category"]

  catalog.append({
   "id": video_id,
   "title": title,
   "category": cats,
   "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
  })

  for c in cats:
   categories[c].append(video_id)


print("Videos categorized:",len(catalog))

os.makedirs("catalog/pages", exist_ok=True)
os.makedirs("catalog/categories", exist_ok=True)

pages = [catalog[i:i+PAGE_SIZE] for i in range(0,len(catalog),PAGE_SIZE)]

for i,page in enumerate(pages,1):

 with open(f"catalog/pages/page{i}.json","w") as f:
  json.dump(page,f,indent=2)


for cat,ids in categories.items():

 with open(f"catalog/categories/{cat}.json","w") as f:
  json.dump(ids,f,indent=2)


with open("catalog/catalog.json","w") as f:
 json.dump(catalog,f,indent=2)

print("Catalog created")
