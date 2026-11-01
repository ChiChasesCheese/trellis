"""Survey and fetch Hello Interview's learn pages (system design + low-level design) without logging in.

    python3 research/hello-interview/fetch.py      # -> research/hello-interview/pages.json, sources/local/hello-interview/

Hello Interview is a commercial prep site: page text stays in gitignored sources/local/ (the repo is public); only the
outline (url, section, title, free or premium, length) is committed. Premium pages are listed but not fetched beyond
their public preview; Chi will give access later.
"""
from __future__ import annotations

import html
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "sources/local/hello-interview"
BASE = "https://www.hellointerview.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
ROOTS = ["/learn/system-design/in-a-hurry/introduction", "/learn/low-level-design/in-a-hurry/introduction"]


def get(path: str) -> str:
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except OSError:
            time.sleep(2 ** i)
    return ""


def text_of(page: str) -> str:
    main = re.search(r"<main[^>]*>(.*?)</main>", page, re.S)
    body = main.group(1) if main else page
    body = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", "", body, flags=re.S)
    body = re.sub(r"<(h[1-6])[^>]*>", lambda m: "\n\n" + "#" * int(m.group(1)[1]) + " ", body)
    body = re.sub(r"<(p|li|br|div|pre|tr)[^>]*>", "\n", body)
    body = re.sub(r"<[^>]+>", "", body)
    return re.sub(r"\n{3,}", "\n\n", html.unescape(body)).strip()


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    links = []
    for r in ROOTS:
        page = get(r)
        part = r.split("/")[2]
        links += [l for l in dict.fromkeys(re.findall(r'href="(/learn/%s/[^"#?]+)"' % part, page))]
    pages = []
    for path in dict.fromkeys(links):
        if path.endswith("/vote"):
            continue
        page = get(path)
        slug = path.removeprefix("/learn/").replace("/", "__")
        (RAW / f"{slug}.html").write_text(page, encoding="utf-8")
        text = text_of(page)
        (RAW / f"{slug}.md").write_text(text, encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", page, re.S)
        parts = path.split("/")
        pages.append({"url": BASE + path, "track": parts[2], "section": parts[3] if len(parts) > 4 else "",
                      "page": parts[-1], "title": html.unescape(title.group(1)).split("|")[0].strip() if title else parts[-1],
                      "premium": 'isPremiumContent\\":true' in page, "chars": len(text)})
        print(f"{'P' if pages[-1]['premium'] else 'F'} {len(text):6} {path}", flush=True)
        time.sleep(0.8)
    (ROOT / "research/hello-interview/pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=1), encoding="utf-8")
    free = sum(not p["premium"] for p in pages)
    print(len(pages), "pages;", free, "free;", len(pages) - free, "premium")


if __name__ == "__main__":
    main()
