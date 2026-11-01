"""LeetCode study dashboard: one self-contained HTML page from the shared problem files, Anki and LeetCode's public API.

    uv run python scripts/lc_dashboard.py            # -> sources/local/dashboard/index.html (gitignored: personal data)

Every problem is keyed by its slug (vault/interviews/core/leetcode/problems/<slug>.md), so the deck cards that point at
it, its list memberships, its TikTok / company-tag frequency, Chi's Anki reviews and his LeetCode solves join on one key.
Mastery of a problem: 0 if never reviewed, else 0.6 * min(1, longest interval / 21 days) + 0.4 * recall over the last
90 days; a knowledge area's mastery is the mean over its problems in LeetCode Tops 01-17 (unseen counts as 0).
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from leetcode_daily import gql  # noqa: E402

OUT = ROOT / "sources/local/dashboard"
PROBLEMS = ROOT / "vault/interviews/core/leetcode/problems"
DAY = 86400


def anki(action: str, **params):
    for _ in range(20):
        try:
            r = json.load(urllib.request.urlopen("http://127.0.0.1:8765", json.dumps(
                {"action": action, "version": 6, "params": params}).encode(), timeout=120))
            if not r.get("error"):
                return r["result"]
        except OSError:
            pass
        time.sleep(2)
    raise SystemExit(f"AnkiConnect: {action} failed")


def problems() -> dict[str, dict]:
    out = {}
    for f in sorted(PROBLEMS.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        h = re.search(r"^\*\*LC (\d+) ([^*\n]+)\*\*｜(\w+)", text, re.M) or re.search(r"^\*\*([^*\n]+)\*\*｜(\w*)", text, re.M)
        kd = re.search(r"\*\*考点。\*\*\s*(.+)", text) or re.search(r"\*\*一句话。\*\*\s*(.+)", text)
        if h and h.lastindex == 3:
            out[f.stem] = {"id": int(h.group(1)), "name": h.group(2).strip(), "diff": h.group(3)}
        else:
            out[f.stem] = {"id": 0, "name": h.group(1).strip() if h else f.stem, "diff": h.group(2) if h else ""}
        out[f.stem]["idea"] = re.sub(r"[`*]", "", kd.group(1))[:90] if kd else ""
    return out


def main() -> None:
    probs = problems()
    tops = yaml.safe_load((ROOT / "skeleton/leetcode-tops.yaml").read_text(encoding="utf-8"))
    area_title = {n["id"]: re.sub(r"（.*?）", "", n["title"]) for n in tops["nodes"]}
    area = {c["id"].split(".", 1)[1]: n["id"] for n in tops["nodes"] for c in n["children"]}
    sel = {p["slug"]: p for p in json.loads((ROOT / "research/leetcode-tops/selection.json").read_text(encoding="utf-8"))}
    tt = json.loads((ROOT / "research/companies/tiktok/index.json").read_text(encoding="utf-8"))
    # decks that carry each problem (stub cards)
    decks: dict[str, set] = defaultdict(set)
    for name, pattern in (("TikTok", "tiktok/cards/*/*.md"), ("Tops", "tops/cards/*/*.md"), ("核心27", "tiktok-core/cards/*/*.md"),
                          ("Daily", "daily/cards/*.md")):
        for f in (ROOT / "vault/interviews/core/leetcode").glob(pattern):
            m = re.search(r"^body: interviews/core/leetcode/problems/(\S+)$", f.read_text(encoding="utf-8"), re.M)
            if m:
                decks[m.group(1)].add(name)

    # Anki: every LeetCode Tops card that has been reviewed, mapped to a problem slug through its hierarchical tag
    cids = anki("findCards", query='"deck:LeetCode Tops*" -is:new')
    info = []
    for i in range(0, len(cids), 400):
        info += anki("cardsInfo", cards=cids[i:i + 400])
    notes = {}
    nids = list({c["note"] for c in info})
    for i in range(0, len(nids), 400):
        for n in anki("notesInfo", notes=nids[i:i + 400]):
            notes[n["noteId"]] = n["tags"]
    reviews = {}
    for i in range(0, len(cids), 300):
        reviews.update(anki("getReviewsOfCards", cards=[str(c) for c in cids[i:i + 300]]))
    now = time.time()
    slug_of = {}
    for c in info:
        for t in notes.get(c["note"], []):
            if t.startswith(("id::", "trellis::")):
                continue
            last = t.split("::")[-1]
            if last in probs or last in sel or last in tt:
                slug_of[c["cardId"]] = last
                break
    per = defaultdict(lambda: {"reviews": 0, "again": 0, "again30": 0, "rev90": 0, "again90": 0, "ivl": 0, "last": 0,
                               "lapses": 0, "cards": 0})
    daily_reviews = defaultdict(lambda: [0, 0])  # date -> [reviews, again]
    area_week = defaultdict(lambda: [0, 0])       # (area, week index back from now) -> [reviews, again]
    deck_of = {c["cardId"]: c["deckName"] for c in info}
    for c in info:
        s = slug_of.get(c["cardId"])
        revs = reviews.get(str(c["cardId"]), [])
        for r in revs:
            ts = r["id"] / 1000
            d = datetime.fromtimestamp(ts).date().isoformat()
            daily_reviews[d][0] += 1
            daily_reviews[d][1] += r["ease"] == 1
            if s and s in area:
                wk = int((now - ts) // (7 * DAY))
                if wk < 12:
                    area_week[(area[s], wk)][0] += 1
                    area_week[(area[s], wk)][1] += r["ease"] == 1
        if not s:
            continue
        p = per[s]
        p["cards"] += 1
        p["lapses"] += c["lapses"]
        p["ivl"] = max(p["ivl"], c["interval"])
        for r in revs:
            ts = r["id"] / 1000
            p["reviews"] += 1
            p["again"] += r["ease"] == 1
            p["last"] = max(p["last"], ts)
            if now - ts < 90 * DAY:
                p["rev90"] += 1
                p["again90"] += r["ease"] == 1
            if now - ts < 30 * DAY:
                p["again30"] += r["ease"] == 1

    def mastery(s: str) -> float:
        p = per.get(s)
        if not p or not p["reviews"]:
            return 0.0
        recall = 1 - p["again90"] / p["rev90"] if p["rev90"] else 1 - p["again"] / p["reviews"]
        return round(0.6 * min(1, p["ivl"] / 21) + 0.4 * recall, 3)

    other = json.loads((ROOT / "research/companies/tiktok/catalog/other_lists.json").read_text(encoding="utf-8"))
    classic = json.loads((ROOT / "research/classic-lists/index.json").read_text(encoding="utf-8"))
    by_id = defaultdict(list)
    for s, v in probs.items():
        if v["id"]:
            by_id[v["id"]].append(s)
    lists = {"Blind 75": other["Blind 75"], "NeetCode 150": other["NeetCode 150"], "Hot 100": other["LeetCode Hot 100"],
             "Top Interview 150": other["Top Interview 150"],
             "LeetCode 75": [int(k) for k, v in classic.items() if "LeetCode 75" in v["lists"]]}
    list_slugs = {k: [s for n in v for s in by_id.get(int(n), [])] for k, v in lists.items()}
    list_slugs["TikTok P1–P4"] = [s for s, p in tt.items() if p.get("band", "").startswith("p")]
    list_slugs["LeetCode Tops 372"] = list(sel)

    rows = []
    for s, v in probs.items():
        p = per.get(s, {})
        rows.append({"s": s, "id": v["id"], "n": v["name"], "d": v["diff"], "k": v["idea"], "a": area.get(s, ""),
                     "dk": sorted(decks.get(s, [])), "r": sel.get(s, {}).get("rank"), "tt": tt.get(s, {}).get("band", ""),
                     "l": [k for k, ss in list_slugs.items() if s in ss and k not in ("LeetCode Tops 372",)],
                     "m": mastery(s), "rv": p.get("reviews", 0), "ag": p.get("again", 0), "ag30": p.get("again30", 0),
                     "lp": p.get("lapses", 0), "iv": p.get("ivl", 0),
                     "last": datetime.fromtimestamp(p["last"]).date().isoformat() if p.get("last") else ""})
    row = {r["s"]: r for r in rows}

    areas = []
    for aid, title in area_title.items():
        ss = [s for s, a in area.items() if a == aid]
        seen = [s for s in ss if per.get(s, {}).get("reviews")]
        areas.append({"id": aid, "t": title, "n": len(ss), "seen": len(seen),
                      "mature": sum(1 for s in ss if per.get(s, {}).get("ivl", 0) >= 21),
                      "m": round(sum(mastery(s) for s in ss) / max(len(ss), 1), 3),
                      "str": round(sum(mastery(s) for s in seen) / max(len(seen), 1), 3),
                      "weeks": [[area_week[(aid, w)][0], area_week[(aid, w)][1]] for w in range(11, -1, -1)]})
    cover = []
    for k, ss in list_slugs.items():
        ss = [s for s in dict.fromkeys(ss) if s in row]
        cover.append({"t": k, "n": len(ss), "card": sum(1 for s in ss if row[s]["dk"]),
                      "seen": sum(1 for s in ss if row[s]["rv"]), "mature": sum(1 for s in ss if row[s]["iv"] >= 21),
                      "m": round(sum(row[s]["m"] for s in ss) / max(len(ss), 1), 3)})

    # LeetCode public profile
    user = json.loads((ROOT / "sources/local/leetcode-daily/state.json").read_text(encoding="utf-8"))
    q = ("query($u:String!,$y:Int){matchedUser(username:$u){submitStats{acSubmissionNum{difficulty count}} "
         "tagProblemCounts{advanced{tagName problemsSolved} intermediate{tagName problemsSolved} fundamental{tagName problemsSolved}} "
         "userCalendar(year:$y){streak totalActiveDays submissionCalendar}} "
         "userContestRanking(username:$u){rating attendedContestsCount globalRanking topPercentage} "
         "userContestRankingHistory(username:$u){attended rating contest{title startTime}}}")
    cal = {}
    lc = {}
    for y in (date.today().year - 1, date.today().year):
        d = gql("leetcode.com", q, {"u": user["username"], "y": y})
        lc = d
        for ts, n in json.loads(d["matchedUser"]["userCalendar"]["submissionCalendar"] or "{}").items():
            cal[datetime.fromtimestamp(int(ts)).date().isoformat()] = n
    m = lc["matchedUser"]
    tags = sorted((t for g in m["tagProblemCounts"].values() for t in g), key=lambda t: -t["problemsSolved"])[:16]
    contests = [{"t": h["contest"]["title"], "r": round(h["rating"]), "d": datetime.fromtimestamp(h["contest"]["startTime"]).date().isoformat()}
                for h in lc.get("userContestRankingHistory") or [] if h["attended"]]
    recent = [{"s": s, "d": v["solved"], "n": v.get("title_zh") or v["title"], "id": v["id"], "diff": v["difficulty"]}
              for s, v in sorted(user["seen"].items(), key=lambda kv: kv[1]["solved"], reverse=True)]

    data = {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "rows": rows, "areas": areas, "cover": cover,
            "anki": {d: v for d, v in sorted(daily_reviews.items())}, "lc": cal,
            "solved": {x["difficulty"]: x["count"] for x in m["submitStats"]["acSubmissionNum"]},
            "contest": lc.get("userContestRanking"), "contests": contests[-20:], "tags": tags,
            "streak": m["userCalendar"]["streak"], "active": m["userCalendar"]["totalActiveDays"], "recent": recent}
    OUT.mkdir(parents=True, exist_ok=True)
    html = (ROOT / "scripts/lc_dashboard.html").read_text(encoding="utf-8")
    (OUT / "index.html").write_text(html.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    print(f"{len(rows)} problems, {len(info)} reviewed cards, {sum(v[0] for v in daily_reviews.values())} reviews ->",
          (OUT / "index.html").relative_to(ROOT))


if __name__ == "__main__":
    main()
