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

result = subprocess.run(
 ["yt-dlp","--dump-single-json",CHANNEL],
 capture_output=True,
 text=True
)

data = json.loads(result.stdout)
videos = data.get("entries", [])

catalog = []
categories = {c.lower(): [] for c in CATEGORIES}

for v in videos:

 if not v:
  continue

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
   "id": video_id,
   "title": title,
   "category": video_categories,
   "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
  })

print(f"Videos categorized: {len(catalog)}")

os.makedirs("catalog/pages",exist_ok=True)
os.makedirs("catalog/categories",exist_ok=True)

pages=[catalog[i:i+PAGE_SIZE] for i in range(0,len(catalog),PAGE_SIZE)]

for i,page in enumerate(pages,1):

 with open(f"catalog/pages/page{i}.json","w") as f:
  json.dump(page,f,indent=2)

for cat,ids in categories.items():

 with open(f"catalog/categories/{cat}.json","w") as f:
  json.dump(ids,f,indent=2)

print("Catalog created")
