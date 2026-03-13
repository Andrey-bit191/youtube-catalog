import json
import subprocess
import os

CHANNEL = "https://www.youtube.com/@PulseSignalOfficial"

CATEGORIES = {
 "master": "#Master",
 "remaster": "#Remaster",
 "live": "#Live",
 "jungle": "#Jungle",
 "club": "#Club",
 "dance": "#Dance",
 "piano": "#Piano"
}

PAGE_SIZE = 20

print("Scanning channel...")

result = subprocess.run(
 ["yt-dlp","--dump-json","--playlist-end","2000",CHANNEL],
 capture_output=True,
 text=True
)

print(result.stdout[:1000])

videos = []

for line in result.stdout.splitlines():
 try:
  data = json.loads(line)
  videos.append(data)
 except:
  pass

catalog = []
categories = {k: [] for k in CATEGORIES}

for v in videos:

 video_id = v["id"]
 title = v["title"]

 url = f"https://youtube.com/watch?v={video_id}"

 desc = subprocess.run(
  ["yt-dlp","--dump-json",url],
  capture_output=True,
  text=True
 )

 try:
  info = json.loads(desc.stdout)
  description = info.get("description","")
 except:
  description = ""

 video_categories = []

 for cat,tag in CATEGORIES.items():
  if tag.lower() in description.lower():
   video_categories.append(cat)
   categories[cat].append(video_id)

 if video_categories:

  catalog.append({
   "id":video_id,
   "title":title,
   "category":video_categories,
   "thumbnail":f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
  })

os.makedirs("catalog/pages",exist_ok=True)
os.makedirs("catalog/categories",exist_ok=True)

pages=[catalog[i:i+PAGE_SIZE] for i in range(0,len(catalog),PAGE_SIZE)]

for i,page in enumerate(pages,1):

 with open(f"catalog/pages/page{i}.json","w") as f:
  json.dump(page,f,indent=2)

for cat,ids in categories.items():

 with open(f"catalog/categories/{cat}.json","w") as f:
  json.dump(ids,f)

print("Catalog created")
