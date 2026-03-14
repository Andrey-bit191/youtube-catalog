name: Scan Private Videos

on:
  workflow_dispatch:

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:

      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install yt-dlp
        run: |
          pip install yt-dlp

      - name: Run private scanner
        run: |
          python scripts/private_scanner.py

      - name: Commit results
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "actions@github.com"
          git add catalog/private_videos.json
          git commit -m "Update private videos" || echo "No changes"
          git push
