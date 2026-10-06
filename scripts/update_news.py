"""Refresh the same-origin, mixed-source headlines shown on the display."""

import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


FEEDS = (
    ("BBC News", "https://feeds.bbci.co.uk/news/uk/rss.xml", "https://www.bbc.co.uk/news/"),
    ("Sky News", "https://feeds.skynews.com/feeds/rss/home.xml", "https://news.sky.com/"),
)
MEDIA = "{http://search.yahoo.com/mrss/}"
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


by_source = []
for source, feed_url, link_prefix in FEEDS:
    try:
        request = urllib.request.Request(feed_url, headers={"User-Agent": "StudyCentreDisplay/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            feed = ET.fromstring(response.read())
    except (OSError, ET.ParseError) as error:
        print(f"{source} unavailable: {error}")
        continue
    source_items = []
    for entry in feed.findall("./channel/item"):
        title = clean(entry.findtext("title"))
        summary = clean(entry.findtext("description"))
        link = (entry.findtext("link") or "").strip()
        if not title or not summary or not link.startswith(link_prefix):
            continue
        image = ""
        for tag in (MEDIA + "thumbnail", MEDIA + "content", "enclosure"):
            media = entry.find(tag)
            if media is not None and (media.get("url") or "").startswith("https://"):
                image = media.get("url")
                break
        source_items.append({"title": title, "summary": short_summary(summary), "link": link,
                             "source": source, "image": image})
        if len(source_items) == 3:
            break
    by_source.append(source_items)

items = []
for position in range(3):
    for source_items in by_source:
        if position < len(source_items):
            items.append(source_items[position])

if len(items) < 3:
    raise RuntimeError("News feeds returned fewer than three usable stories; keeping the previous news file")

payload = {"updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "items": items}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
