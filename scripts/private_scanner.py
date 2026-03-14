import json
import subprocess
import re
import os

CATEGORIES = [
 "Master",
 "Remaster",
 "Live",
 "Jungle",
 "Club",
 "Dance",
 "Piano"
]

LINKS_FILE = "private_links.txt"
OUTPUT_FILE = "catalog/private_videos.json"

def detect_category(title):

 result = []

 for cat in CATEGORIES:

  pattern = r"\(" + cat + r"\)"

  if re.search(pattern,title,re.IGNORECASE):
   result.append(cat.lower())

 return result


if not os.path.exists(LINKS_FILE):

 print("private_links.txt not found")
 exit()


with open(LINKS_FILE) as f:
 links = [l.strip() for l in f.readlines() if l.strip()]


private_videos = []

if os.path.exists(OUTPUT_FILE):

 with open(OUTPUT_FILE) as f:
  private_videos = json.load(f)


existing_ids = {v["id"] for v in private_videos}

for link in links:

 print("Scanning:",link)

 if "watch?v=" in link:
 video_id = link.split("watch?v=")[-1]

elif "youtu.be/" in link:
 video_id = link.split("youtu.be/")[-1]

else:
 print("Unknown link format:", link)
 continue

 if video_id in existing_ids:
  print("Already exists:",video_id)
  continue

 process = subprocess.run(
  ["yt-dlp","--dump-json",link],
  capture_output=True,
  text=True
 )

 try:

  data = json.loads(process.stdout)

  title = data.get("title","")

  cats = detect_category(title)

  if not cats:
   print("No category detected:",title)
   continue

  video = {
   "id": video_id,
   "title": title,
   "category": cats
  }

  private_videos.append(video)

  print("Added:",title,cats)

 except:

  print("Error reading video:",link)


os.makedirs("catalog",exist_ok=True)

with open(OUTPUT_FILE,"w") as f:
 json.dump(private_videos,f,indent=2)


print("Private videos updated:",len(private_videos))
