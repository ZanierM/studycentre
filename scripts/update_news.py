"""Refresh the same-origin BBC headlines shown on the Study Centre display."""

import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


FEED_URL = "https://feeds.bbci.co.uk/news/uk/rss.xml"
OUTPUT = Path(__file__).resolve().parents[1] / "news.json"


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def clean(value):
    parser = PlainText()
    parser.feed(unescape(value or ""))
    return re.sub(r"\s+", " ", "".join(parser.parts)).strip()


def short_summary(value):
    if len(value) <= 190:
        return value
    return value[:190].rsplit(" ", 1)[0].rstrip(" ,;:") + "…"


request = urllib.request.Request(FEED_URL, headers={"User-Agent": "StudyCentreDisplay/1.0"})
with urllib.request.urlopen(request, timeout=20) as response:
    feed = ET.fromstring(response.read())

items = []
seen = set()
for entry in feed.findall("./channel/item"):
    title = clean(entry.findtext("title"))
    summary = clean(entry.findtext("description"))
    link = (entry.findtext("link") or "").strip()
    if not title or not summary or not link.startswith("https://www.bbc.co.uk/news/") or link in seen:
        continue
    seen.add(link)
    items.append({"title": title, "summary": short_summary(summary), "link": link})
    if len(items) == 6:
        break

if len(items) < 3:
    raise RuntimeError("BBC RSS returned fewer than three usable stories; keeping the previous news file")

payload = {"updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "items": items}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
