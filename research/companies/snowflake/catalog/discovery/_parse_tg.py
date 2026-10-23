import re
import json
import html as htmllib
from pathlib import Path

DIR = Path(__file__).parent / "mirror_1p3a_snowflake"


def parse_page(path):
    raw = path.read_text(encoding="utf-8")
    parts = re.split(r'(?=<div class="tgme_widget_message_wrap)', raw)
    out = []
    for part in parts:
        m = re.search(r'data-post="usinterview/(\d+)"', part)
        if not m:
            continue
        pid = m.group(1)
        dt = re.search(r'<time datetime="([^"]+)"', part)
        datetime_ = dt.group(1) if dt else ""
        txt_m = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', part, re.S)
        text_raw = txt_m.group(1) if txt_m else ""
        text = re.sub(r"<[^>]+>", " ", text_raw)
        text = htmllib.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        title_m = re.search(r'<div class="link_preview_title"[^>]*>(.*?)</div>', part, re.S)
        title = re.sub(r"<[^>]+>", "", title_m.group(1)) if title_m else ""
        title = htmllib.unescape(title).strip()
        desc_m = re.search(r'<div class="link_preview_description"[^>]*>(.*?)</div>', part, re.S)
        desc = re.sub(r"<[^>]+>", "", desc_m.group(1)) if desc_m else ""
        desc = htmllib.unescape(desc).strip()
        link_m = re.search(r'href="(https?://(?:www\.)?1point3acres\.com/bbs/thread-(\d+)[^"]*)"', part)
        p3a_url = link_m.group(1) if link_m else ""
        p3a_id = link_m.group(2) if link_m else ""
        out.append(
            {
                "id": pid,
                "tg_url": f"https://t.me/usinterview/{pid}",
                "datetime": datetime_,
                "text": text,
                "title": title,
                "desc": desc,
                "1p3a_url": p3a_url,
                "1p3a_id": p3a_id,
            }
        )
    return out


def main():
    all_posts = {}
    for pg in ["page_1.html", "page_2.html"]:
        for p in parse_page(DIR / pg):
            all_posts[p["id"]] = p
    posts = sorted(all_posts.values(), key=lambda x: x["datetime"], reverse=True)
    (DIR / "_parsed.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(posts))
    for p in posts:
        print(p["datetime"], p["id"], p["1p3a_id"], p["title"][:40])


if __name__ == "__main__":
    main()
