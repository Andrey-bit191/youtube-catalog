import json
import re
import os

LINKS_FILE = "private_links.txt"
OUTPUT_FILE = "catalog/private_videos.json"

CATEGORIES = [
    "master",
    "remaster",
    "live",
    "jungle",
    "club",
    "dance",
    "piano"
]


def extract_video_id(link):

    if "watch?v=" in link:
        return link.split("watch?v=")[-1]

    if "youtu.be/" in link:
        return link.split("youtu.be/")[-1]

    return None


def detect_category(text):

    text = text.lower()

    for cat in CATEGORIES:
        if f"({cat})" in text:
            return [cat]

    return []


if not os.path.exists(LINKS_FILE):
    print("private_links.txt not found")
    exit()


with open(LINKS_FILE) as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]


private_videos = []

if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE) as f:
            private_videos = json.load(f)
    except:
        private_videos = []


existing_ids = {v["id"] for v in private_videos}


for line in lines:

    print("Processing:", line)

    parts = line.split("|")

    link = parts[0].strip()

    title = ""

    if len(parts) > 1:
        title = parts[1].strip()

    video_id = extract_video_id(link)

    if not video_id:
        print("Invalid link:", link)
        continue

    if video_id in existing_ids:
        print("Already exists:", video_id)
        continue

    cats = detect_category(title)

    if not cats:
        print("Category not detected in title:", title)
        continue

    video = {
        "id": video_id,
        "title": title,
        "category": cats
    }

    private_videos.append(video)

    print("Added:", title)


os.makedirs("catalog", exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    json.dump(private_videos, f, indent=2)


print("Private videos updated:", len(private_videos))
