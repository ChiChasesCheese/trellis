"""Save Hello Interview pages through Chi's logged-in Chrome, one at a time, into gitignored sources/local/.

    python3 research/hello-interview/chrome_fetch.py pages            # every course page in pages.json + sections
    python3 research/hello-interview/chrome_fetch.py questions        # the whole question bank, plus TikTok / ByteDance
    python3 research/hello-interview/chrome_fetch.py url <url> <out>  # one page, for probing

Chrome's own `save` AppleScript verb writes the page; nothing reads Chrome's cookies or profile, and JavaScript from
Apple Events stays off. Works in one dedicated background tab, found by id so Chi's tabs are never navigated, and
closes it at the end. Sequential with a pause. Re-running skips what is already saved. Everything saved stays in
sources/local/ because the site is commercial and the repo is public.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sources/local/hello-interview/premium"
BASE = "https://www.hellointerview.com"
PAUSE = 2.0
SIGNED_IN = "Chi Zhang"

SCRIPT = r'''
on findTab(theId)
  tell application "Google Chrome"
    repeat with w in windows
      repeat with t in tabs of w
        if ((id of t) as text) is (theId as text) then return t
      end repeat
    end repeat
  end tell
  error "tab gone"
end findTab

on run argv
  set cmd to item 1 of argv
  if cmd is "open" then
    tell application "Google Chrome"
      set w to window 1
      set keep to active tab index of w
      set t to make new tab at end of tabs of w with properties {URL:"about:blank"}
      set active tab index of w to keep
      return id of t
    end tell
  end if
  set t to my findTab(item 2 of argv)
  if cmd is "close" then
    tell application "Google Chrome" to close t
    return "closed"
  end if
  set outFile to POSIX file (item 4 of argv)
  tell application "Google Chrome"
    set URL of t to (item 3 of argv)
    delay 1
    repeat 80 times
      delay 0.5
      if not (loading of t) then exit repeat
    end repeat
    delay (item 6 of argv) as number
    save t in outFile as (item 5 of argv)
    delay 1.5
    return title of t
  end tell
end run
'''


class Tab:
    """The one tab this tool owns."""

    def __init__(self) -> None:
        self.dir = Path(tempfile.mkdtemp(prefix="hi-chrome-", dir="/private/tmp"))
        self.scpt = self.dir / "tab.scpt"
        self.scpt.write_text(SCRIPT, encoding="utf-8")
        self.id = self._osa("open")

    def _osa(self, *args: str) -> str:
        r = subprocess.run(["osascript", str(self.scpt), *args], capture_output=True, text=True, timeout=120)
        if r.returncode:
            raise RuntimeError(r.stderr.strip()[:300])
        return r.stdout.strip()

    def save(self, url: str, dest: Path, rendered: bool = False, settle: float = 2.0) -> str:
        """rendered=True saves the live DOM (for client-rendered pages), otherwise the served HTML."""
        tmp = self.dir / "page.html"
        kind = "complete html" if rendered else "only html"
        title = self._osa("go", self.id, url, str(tmp), kind, str(settle))
        for _ in range(40):
            if tmp.exists() and tmp.stat().st_size:
                break
            time.sleep(0.5)
        if not tmp.exists():
            raise RuntimeError(f"nothing saved for {url}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(tmp), dest)
        shutil.rmtree(self.dir / "page_files", ignore_errors=True)
        return title

    def close(self) -> None:
        self._osa("close", self.id)
        shutil.rmtree(self.dir, ignore_errors=True)


def page_text(page: str) -> str:
    """Article text with headings, list items and code kept, in reading order."""
    main = re.search(r"<main[^>]*>(.*?)</main>", page, re.S)
    body = main.group(1) if main else page
    body = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", "", body, flags=re.S)
    body = re.sub(r"<pre[^>]*>(.*?)</pre>", lambda m: "\n```\n" + re.sub(r"<[^>]+>", "", m.group(1)) + "\n```\n", body, flags=re.S)
    body = re.sub(r"<(h[1-6])[^>]*>", lambda m: "\n\n" + "#" * int(m.group(1)[1]) + " ", body)
    body = re.sub(r"<li[^>]*>", "\n- ", body)
    body = re.sub(r"<(p|br|div|tr|section|blockquote)[^>]*>", "\n", body)
    body = re.sub(r"<[^>]+>", "", body)
    text = re.sub(r"\n{3,}", "\n\n", html.unescape(body)).strip()
    start = re.search(r"^# ", text, re.M)  # drop the side navigation and the footer
    text = text[start.start():] if start else text
    return text.split("\n###### Questions\n", 1)[0].strip()


def fetch_pages(tab: Tab) -> None:
    pages = json.loads((ROOT / "research/hello-interview/pages.json").read_text(encoding="utf-8"))
    report = []
    for i, p in enumerate(pages, 1):
        stem = p["url"].replace(BASE + "/learn/", "").replace("/", "__")
        html_path, txt = OUT / "pages" / f"{stem}.html", OUT / "pages" / f"{stem}.md"
        if not txt.exists():
            title = tab.save(p["url"], html_path)
            raw = html_path.read_text(encoding="utf-8", errors="replace")
            if SIGNED_IN not in raw:
                raise SystemExit(f"not signed in at {p['url']}; stopping")
            txt.write_text(f"# {title}\n\n{page_text(raw)}\n", encoding="utf-8")
            time.sleep(PAUSE)
        report.append({"stem": stem, "premium_before": p["premium"], "chars": len(txt.read_text(encoding="utf-8"))})
        print(f"{i:3}/{len(pages)} {stem} {report[-1]['chars']}", flush=True)
    (OUT / "pages_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")


def questions_url(company: str | None, page: int) -> str:
    keys = ("company", "interviewTypes", "interviewLevels", "regions", "patternId", "search")
    j = {"company": company, "interviewTypes": None, "interviewLevels": None, "regions": None, "patternId": None,
         "search": None, "sort": "recentAndPopular", "page": page, "pageSize": 25, "atLeastOneUpvote": True}
    inp = {"0": {"json": j, "meta": {"values": {k: ["undefined"] for k in keys if j[k] is None}}}}
    return f"{BASE}/trpc/intelligence/getQuestionsAndUpvotes?batch=1&input=" + urllib.parse.quote(json.dumps(inp, separators=(",", ":")))


def read_questions(path: Path) -> dict:
    t = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<pre[^>]*>(.*?)</pre>", t, re.S)
    return json.loads(html.unescape(m.group(1)) if m else t)[0]["result"]["data"]["json"]


def fetch_questions(tab: Tab) -> None:
    seen: dict[str, dict] = {}
    for company, name in ((None, "all"), ("TikTok", "tiktok"), ("ByteDance", "bytedance")):
        page, total = 1, 1
        while page <= total:
            dest = OUT / "questions" / f"{name}-{page:03}.json"
            if not dest.exists():
                tab.save(questions_url(company, page), dest)
                time.sleep(PAUSE)
            d = read_questions(dest)
            total = d.get("totalPages") or 0
            for q in d.get("questions", []):
                seen.setdefault(q["id"], q)
            print(f"{name} {page}/{total} seen {len(seen)}", flush=True)
            page += 1
    (OUT / "questions.json").write_text(json.dumps(list(seen.values()), ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> int:
    cmd = sys.argv[1]
    tab = Tab()
    try:
        if cmd == "pages":
            fetch_pages(tab)
        elif cmd == "questions":
            fetch_questions(tab)
        elif cmd == "url":
            print(tab.save(sys.argv[2], Path(sys.argv[3]), rendered=len(sys.argv) > 4, settle=5.0))
    finally:
        tab.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
