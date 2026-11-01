"""Collect Hello Interview's publicly visible question bank.

    python3 research/hello-interview/fetch_questions.py

An anonymous visitor sees the 25 top "recent and popular" questions and, on each company page, that company's top 5
(the rest, and the type / level filters, are premium). This walks the same two views: the overall list, then every
company that appears in the reports seen so far (breadth-first, up to MAX_COMPANIES). Records keep each question's
reports (company, level, region, month); full text stays in sources/local/hello-interview/questions.json (gitignored),
and research/hello-interview/questions.json keeps titles, type, report counts and links.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
MAX_COMPANIES = 250
KEYS = ("company", "interviewTypes", "interviewLevels", "regions", "patternId", "search")


def visible(company: str | None) -> dict:
    j = {"company": company, "interviewTypes": None, "interviewLevels": None, "regions": None, "patternId": None,
         "search": None, "sort": "recentAndPopular", "page": 1, "pageSize": 25, "atLeastOneUpvote": True}
    inp = {"0": {"json": j, "meta": {"values": {k: ["undefined"] for k in KEYS if j[k] is None}}}}
    url = ("https://www.hellointerview.com/trpc/intelligence/getQuestionsAndUpvotes?batch=1&input="
           + urllib.parse.quote(json.dumps(inp, separators=(",", ":"))))
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.hellointerview.com/community/questions"})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())[0]["result"]["data"]["json"]
        except OSError:
            time.sleep(2 ** i)
    return {"questions": [], "totalCount": 0}


def main() -> None:
    seen: dict[str, dict] = {}
    totals: dict[str, int] = {}
    queue, done = [None], set()
    while queue and len(done) < MAX_COMPANIES:
        c = queue.pop(0)
        if c in done:
            continue
        done.add(c)
        d = visible(c)
        totals[c or "ALL"] = d.get("totalCount", 0)
        for q in d.get("questions", []):
            if not q.get("slug") or "lorem" in (q.get("title") or "").lower():
                continue
            seen.setdefault(q["id"], q)
            for u in q.get("upvotes") or []:
                if u.get("company") and u["company"] not in done and u["company"] not in queue:
                    queue.append(u["company"])
        print(f"{len(done):3} {c or 'ALL':28} total {d.get('totalCount', 0):5}  questions so far {len(seen)}", flush=True)
        time.sleep(0.8)
    qs = list(seen.values())
    (ROOT / "sources/local/hello-interview/questions.json").write_text(json.dumps(qs, ensure_ascii=False, indent=1), encoding="utf-8")
    slim = [{"id": q["id"], "slug": q["slug"], "title": q["title"], "type": q.get("defaultInterviewType"),
             "reports": len(q.get("upvotes") or []), "breakdown": q.get("detailsLink") or "",
             "url": f"https://www.hellointerview.com/community/questions/{q['slug']}/{q['id']}",
             "companies": sorted({u["company"] for u in q.get("upvotes") or [] if u.get("company")}),
             "last": max((u.get("approxAskedOn") or "")[:10] for u in q.get("upvotes") or [{}])} for q in qs]
    slim.sort(key=lambda x: -x["reports"])
    (ROOT / "research/hello-interview/questions.json").write_text(
        json.dumps({"companies_seen": len(done), "totals": totals, "questions": slim}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(qs), "visible questions from", len(done), "views")


if __name__ == "__main__":
    main()
