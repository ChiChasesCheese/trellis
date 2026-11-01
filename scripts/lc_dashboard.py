"""Study dashboard for the LeetCode decks: what Anki says Chi has studied, how well, and what to do next.

    uv run python scripts/lc_dashboard.py build                         # -> sources/local/dashboard/index.html (static)
    uv run python scripts/lc_dashboard.py serve --host <ip> --minutes 30 # live: every page load re-reads Anki

Anki is the only source for the study numbers (reviews, streak, mastery, coverage, feedback); the LeetCode profile is a
side panel, cached for six hours. Everything joins on the problem slug: the shared body
`vault/interviews/core/leetcode/problems/<slug>.md`, the deck stubs pointing at it, and each Anki note's hierarchical tag
`<domain>::...::<slug>`. To reuse this for another subject, change SUBJECT: the Anki deck root, the item files, how a tag
names an item, and the grouping (here the LeetCode Tops topic branches).

Mastery of an item: 0 if never reviewed, else 0.6 * min(1, longest interval / 21 days) + 0.4 * recall over the last
90 days. A group's mastery is the mean over its items (unseen counts as 0).
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import re
import sys
import threading
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
DAY = 86400
SUBJECT = {
    "deck_root": "LeetCode Tops",
    "items": ROOT / "vault/interviews/core/leetcode/problems",
    "groups_skeleton": ROOT / "skeleton/leetcode-tops.yaml",  # top-level branches = groups
    # the decks shown in the per-deck panel: label -> regex on the Anki deck name
    "decks": {"Tops 01–17": r"^LeetCode Tops::(0\d|1[0-7]) ", "TikTok 整题 24": r"^LeetCode Tops::24 ",
              "TikTok 拆分 25": r"^LeetCode Tops::25 ", "通用核心 27": r"^LeetCode Tops::27 ", "Daily 28": r"^LeetCode Tops::28 "},
}


def anki(action: str, **params):
    for _ in range(20):
        try:
            r = json.load(urllib.request.urlopen("http://127.0.0.1:8765", json.dumps(
                {"action": action, "version": 6, "params": params}).encode(), timeout=120))
            if not r.get("error"):
                return r["result"]
        except OSError:
            pass
        time.sleep(1.5)
    raise RuntimeError(f"AnkiConnect: {action} failed")


def items() -> dict[str, dict]:
    out = {}
    for f in sorted(SUBJECT["items"].glob("*.md")):
        text = f.read_text(encoding="utf-8")
        h = re.search(r"^\*\*LC (\d+) ([^*\n]+)\*\*｜(\w+)", text, re.M)
        g = re.search(r"^\*\*([^*\n]+)\*\*｜(\w*)", text, re.M)
        kd = re.search(r"\*\*考点。\*\*\s*(.+)", text) or re.search(r"\*\*一句话。\*\*\s*(.+)", text)
        out[f.stem] = ({"id": int(h.group(1)), "name": h.group(2).strip(), "diff": h.group(3)} if h else
                       {"id": 0, "name": g.group(1).strip() if g else f.stem, "diff": g.group(2) if g else ""})
        out[f.stem]["idea"] = re.sub(r"[`*]", "", kd.group(1))[:90] if kd else ""
    return out


def deck_label(name: str) -> str:
    for label, rx in SUBJECT["decks"].items():
        if re.match(rx, name):
            return label
    return ""


def collect_anki() -> dict:
    probs = items()
    sk = yaml.safe_load(SUBJECT["groups_skeleton"].read_text(encoding="utf-8"))
    gtitle = {n["id"]: re.sub(r"（.*?）", "", n["title"]) for n in sk["nodes"]}
    group = {c["id"].split(".", 1)[1]: n["id"] for n in sk["nodes"] for c in n["children"]}
    sel = {p["slug"]: p for p in json.loads((ROOT / "research/leetcode-tops/selection.json").read_text(encoding="utf-8"))}
    tt = json.loads((ROOT / "research/companies/tiktok/index.json").read_text(encoding="utf-8"))

    cids = anki("findCards", query=f'"deck:{SUBJECT["deck_root"]}*"')
    info = []
    for i in range(0, len(cids), 500):
        info += anki("cardsInfo", cards=cids[i:i + 500])
    tags = {}
    nids = list({c["note"] for c in info})
    for i in range(0, len(nids), 500):
        for n in anki("notesInfo", notes=nids[i:i + 500]):
            tags[n["noteId"]] = n["tags"]
    seen_ids = [c["cardId"] for c in info if c["reps"] > 0]
    reviews = {}
    for i in range(0, len(seen_ids), 400):
        reviews.update(anki("getReviewsOfCards", cards=[str(c) for c in seen_ids[i:i + 400]]))

    def slug_of(c: dict) -> str:
        for t in tags.get(c["note"], []):
            last = t.split("::")[-1]
            if not t.startswith(("id::", "trellis::")) and (last in probs or last in sel or last in tt):
                return last
        return ""

    now = time.time()
    today = datetime.now().date()
    per = defaultdict(lambda: {"rv": 0, "ag": 0, "ag7": 0, "ag14": 0, "ag30": 0, "rv90": 0, "ag90": 0, "iv": 0, "last": 0})
    by_day = defaultdict(lambda: [0, 0, 0])   # date -> [reviews, again, first-time]
    gweek = defaultdict(lambda: [0, 0])        # (group, weeks back) -> [reviews, again]
    deck_items = defaultdict(set)
    deck_seen = defaultdict(set)
    for c in info:
        s = slug_of(c)
        label = deck_label(c["deckName"])
        if s and label:
            deck_items[label].add(s)
        revs = sorted(reviews.get(str(c["cardId"]), []), key=lambda r: r["id"])
        for i, r in enumerate(revs):
            ts = r["id"] / 1000
            d = datetime.fromtimestamp(ts).date().isoformat()
            by_day[d][0] += 1
            by_day[d][1] += r["ease"] == 1
            by_day[d][2] += i == 0
            if s and s in group and now - ts < 12 * 7 * DAY:
                w = int((now - ts) // (7 * DAY))
                gweek[(group[s], w)][0] += 1
                gweek[(group[s], w)][1] += r["ease"] == 1
        if not s or not revs:
            continue
        if label:
            deck_seen[label].add(s)
        p = per[s]
        p["iv"] = max(p["iv"], c["interval"])
        for r in revs:
            ts, bad = r["id"] / 1000, r["ease"] == 1
            p["rv"] += 1
            p["ag"] += bad
            p["last"] = max(p["last"], ts)
            for days, key in ((7, "ag7"), (14, "ag14"), (30, "ag30")):
                if now - ts < days * DAY:
                    p[key] += bad
            if now - ts < 90 * DAY:
                p["rv90"] += 1
                p["ag90"] += bad

    def mastery(s: str) -> float:
        p = per.get(s)
        if not p or not p["rv"]:
            return 0.0
        recall = 1 - (p["ag90"] / p["rv90"] if p["rv90"] else p["ag"] / p["rv"])
        return round(0.6 * min(1, p["iv"] / 21) + 0.4 * recall, 3)

    # the items a deck of Chi's actually carries (what "studied / total" is measured against)
    in_decks = set().union(*deck_items.values()) if deck_items else set()
    other = json.loads((ROOT / "research/companies/tiktok/catalog/other_lists.json").read_text(encoding="utf-8"))
    classic = json.loads((ROOT / "research/classic-lists/index.json").read_text(encoding="utf-8"))
    by_id = defaultdict(list)
    for s, v in probs.items():
        if v["id"]:
            by_id[v["id"]].append(s)
    lists = {"Blind 75": other["Blind 75"], "NeetCode 150": other["NeetCode 150"], "Hot 100": other["LeetCode Hot 100"],
             "Top Interview 150": other["Top Interview 150"],
             "LeetCode 75": [int(k) for k, v in classic.items() if "LeetCode 75" in v["lists"]]}
    list_slugs = {k: list(dict.fromkeys(s for n in v for s in by_id.get(int(n), []))) for k, v in lists.items()}
    list_slugs["TikTok P1–P4"] = [s for s, p in tt.items() if p.get("band", "").startswith("p") and s in probs]

    rows = []
    for s in sorted(in_decks):
        v, p = probs.get(s, {"id": 0, "name": s, "diff": "", "idea": ""}), per.get(s, {})
        rows.append({"s": s, "id": v["id"], "n": v["name"], "d": v["diff"], "k": v["idea"], "a": group.get(s, ""),
                     "dk": sorted(lb for lb, ss in deck_items.items() if s in ss), "r": sel.get(s, {}).get("rank"),
                     "l": [k for k, ss in list_slugs.items() if s in ss], "m": mastery(s), "rv": p.get("rv", 0),
                     "ag": p.get("ag", 0), "ag7": p.get("ag7", 0), "ag14": p.get("ag14", 0), "ag30": p.get("ag30", 0),
                     "iv": p.get("iv", 0), "last": datetime.fromtimestamp(p["last"]).date().isoformat() if p.get("last") else ""})
    row = {r["s"]: r for r in rows}

    groups = []
    for gid, title in gtitle.items():
        ss = [s for s, g in group.items() if g == gid and s in row]
        seen = [s for s in ss if row[s]["rv"]]
        groups.append({"id": gid, "t": title, "n": len(ss), "seen": len(seen), "mature": sum(row[s]["iv"] >= 21 for s in ss),
                       "m": round(sum(row[s]["m"] for s in ss) / max(len(ss), 1), 3),
                       "weeks": [gweek[(gid, w)] for w in range(11, -1, -1)]})
    cover = [{"t": k, "n": len(ss), "seen": sum(1 for s in ss if s in row and row[s]["rv"]),
              "mature": sum(1 for s in ss if s in row and row[s]["iv"] >= 21),
              "m": round(sum(row[s]["m"] for s in ss if s in row) / max(len(ss), 1), 3)} for k, ss in list_slugs.items()]

    stats = anki("getDeckStats", decks=[SUBJECT["deck_root"]] + sorted({c["deckName"].split("::")[0] + "::" + c["deckName"].split("::")[1]
                                                                          for c in info if "::" in c["deckName"]}))
    due = {}
    for st in stats.values():
        label = deck_label(st["name"] + " ") if st["name"] != SUBJECT["deck_root"] else "all"
        if label:
            d = due.setdefault(label, [0, 0, 0])
            d[0] += st["new_count"]
            d[1] += st["learn_count"]
            d[2] += st["review_count"]
    decks = [{"t": lb, "n": len(deck_items[lb]), "seen": len(deck_seen[lb]), "new": due.get(lb, [0, 0, 0])[0],
              "due": sum(due.get(lb, [0, 0, 0])[1:]),
              "any": sum(1 for s in deck_items[lb] if per.get(s, {}).get("rv"))}  # studied in this or another deck
             for lb in SUBJECT["decks"] if lb in deck_items]

    # streak and recent windows, all from the review log of these decks
    days = {d for d, v in by_day.items() if v[0]}
    streak, d = 0, today if today.isoformat() in days else today - timedelta(days=1)
    while d.isoformat() in days:
        streak, d = streak + 1, d - timedelta(days=1)

    def window(a: int, b: int) -> list[int]:
        tot = [0, 0, 0]
        for i in range(a, b):
            v = by_day.get((today - timedelta(days=i)).isoformat())
            if v:
                tot = [x + y for x, y in zip(tot, v)]
        return tot

    w7, w7p, t0 = window(0, 7), window(7, 14), window(0, 1)

    # feedback from recent answers
    fails7 = sorted((r for r in rows if r["ag7"]), key=lambda r: (-r["ag7"], r["m"]))
    repeat = [r for r in rows if r["ag14"] >= 2]
    gfail = defaultdict(lambda: [0, 0])
    for (g, w), (n, a) in gweek.items():
        if w == 0:
            gfail[g][0] += n
            gfail[g][1] += a
    worst = sorted(((g, a / n, n) for g, (n, a) in gfail.items() if n >= 5), key=lambda x: x[1], reverse=True)[:3]
    handwrite = sorted((r for r in rows if r["rv"]), key=lambda r: -(r["ag14"] * 3 + r["ag"] + (1 - r["m"]) * 2))[:6]
    unseen_hot = sorted((r for r in rows if r["r"] and not r["rv"]), key=lambda r: r["r"])[:5]
    feedback = {"fails7": [r["s"] for r in fails7[:10]], "repeat": [r["s"] for r in repeat],
                "worst": [{"g": gtitle.get(g, g), "rate": round(x, 3), "n": n} for g, x, n in worst],
                "handwrite": [r["s"] for r in handwrite], "unseen_hot": [r["s"] for r in unseen_hot]}

    # 必读: computed, never asked. Chi studies in bursts, so each problem's recall is estimated from the time since its
    # last review against its longest interval (power forgetting curve R = (1 + t / 9S)^-1, S ~ interval), then weighed
    # by how often he forgets it, how recently, and how much it matters; hard problems he just solved on LeetCode and has
    # not yet reviewed join the list.
    last_any = max((r["last"] for r in rows if r["last"]), default="")
    gap = (today - date.fromisoformat(last_any)).days if last_any else 0
    must = []
    for r in rows:
        if not r["rv"]:
            continue
        stab = max(r["iv"], 1)
        elapsed = (today - date.fromisoformat(r["last"])).days if r["last"] else 0
        recall = (1 + elapsed / (9 * stab)) ** -1
        lapse = (r["ag"] + 1) / (r["rv"] + 2)
        weight = 1 + (0.5 if tt.get(r["s"], {}).get("band", "").startswith("p") else 0) + (0.3 if (r["r"] or 999) <= 150 else 0)
        score = weight * ((1 - recall) + lapse) + 0.6 * r["ag14"]
        why = []
        if r["ag14"]:
            why.append(f"14 天内忘了 {r['ag14']} 次")
        if lapse >= 0.34 and r["ag"] >= 2:
            why.append(f"总共忘了 {r['ag']}/{r['rv']} 次")
        if recall < 0.85:
            why.append(f"{elapsed} 天没看，估计还记得 {round(recall * 100)}%")
        if weight > 1.4:
            why.append("高频")
        must.append({"s": r["s"], "score": round(score, 3), "recall": round(recall, 2), "why": why})
    must.sort(key=lambda x: -x["score"])
    must = [m for m in must if m["why"]][:15]
    user = json.loads((ROOT / "sources/local/leetcode-daily/state.json").read_text(encoding="utf-8"))
    for slug, v in sorted(user["seen"].items(), key=lambda kv: kv[1]["solved"], reverse=True):
        if (today - date.fromisoformat(v["solved"])).days <= 7 and v.get("difficulty") in ("Hard", "Medium") \
                and slug in row and not row[slug]["rv"]:
            must.append({"s": slug, "score": 0, "recall": None,
                         "why": [f"{v['solved'][5:]} 在 LeetCode 解出（{'困难' if v['difficulty'] == 'Hard' else '中等'}），还没复习过"]})

    return {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "rows": rows, "groups": groups, "cover": cover,
            "must": must, "gap": gap,
            "decks": decks, "byday": {k: v for k, v in sorted(by_day.items())}, "streak": streak, "w7": w7, "w7p": w7p,
            "today": t0, "due_all": sum(d["due"] for d in decks), "new_all": sum(d["new"] for d in decks),
            "feedback": feedback, "total_items": len(rows)}


def collect_lc() -> dict:
    cache = OUT / "lc.json"
    if cache.exists() and time.time() - cache.stat().st_mtime < 6 * 3600:
        return json.loads(cache.read_text(encoding="utf-8"))
    user = json.loads((ROOT / "sources/local/leetcode-daily/state.json").read_text(encoding="utf-8"))
    q = ("query($u:String!,$y:Int){matchedUser(username:$u){submitStats{acSubmissionNum{difficulty count}} "
         "tagProblemCounts{advanced{tagName problemsSolved} intermediate{tagName problemsSolved} fundamental{tagName problemsSolved}} "
         "userCalendar(year:$y){submissionCalendar}} userContestRanking(username:$u){rating attendedContestsCount topPercentage} "
         "userContestRankingHistory(username:$u){attended rating contest{title startTime}}}")
    cal, d = {}, {}
    for y in (date.today().year - 1, date.today().year):
        d = gql("leetcode.com", q, {"u": user["username"], "y": y})
        for ts, n in json.loads(d["matchedUser"]["userCalendar"]["submissionCalendar"] or "{}").items():
            cal[datetime.fromtimestamp(int(ts)).date().isoformat()] = n
    m = d["matchedUser"]
    out = {"cal": cal, "solved": {x["difficulty"]: x["count"] for x in m["submitStats"]["acSubmissionNum"]},
           "contest": d.get("userContestRanking"),
           "contests": [{"t": h["contest"]["title"], "r": round(h["rating"]),
                         "d": datetime.fromtimestamp(h["contest"]["startTime"]).date().isoformat()}
                        for h in d.get("userContestRankingHistory") or [] if h["attended"]][-20:],
           "tags": sorted((t for g in m["tagProblemCounts"].values() for t in g), key=lambda t: -t["problemsSolved"])[:14],
           "recent": [{"s": s, "d": v["solved"], "n": v.get("title_zh") or v["title"], "id": v["id"], "diff": v["difficulty"]}
                      for s, v in sorted(user["seen"].items(), key=lambda kv: kv[1]["solved"], reverse=True)][:30]}
    OUT.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def data() -> dict:
    d = collect_anki()
    try:
        d["lc"] = collect_lc()
    except Exception as e:  # noqa: BLE001 - the side panel must never break the page
        d["lc"] = {"error": str(e)}
    return d


def page(d: dict) -> str:
    return (ROOT / "scripts/lc_dashboard.html").read_text(encoding="utf-8").replace("/*__DATA__*/null", json.dumps(d, ensure_ascii=False))


def serve(host: str, port: int, minutes: float) -> None:
    lock, cache = threading.Lock(), {"t": 0.0, "body": b""}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.split("?")[0] not in ("/", "/index.html", "/data.json"):
                self.send_error(404)
                return
            with lock:  # one Anki read at a time; reuse it for 20 s
                if time.time() - cache["t"] > 20 or "fresh" in self.path:
                    cache["body"] = json.dumps(data(), ensure_ascii=False).encode()
                    cache["t"] = time.time()
                body = cache["body"]
            if self.path.startswith("/data.json"):
                ctype = "application/json"
            else:
                ctype, body = "text/html; charset=utf-8", page(json.loads(body)).encode()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer((host, port), Handler)
    threading.Timer(minutes * 60, srv.shutdown).start()
    print(f"http://{host}:{port}/ for {minutes:g} min", flush=True)
    srv.serve_forever()
    print("stopped", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "serve"])
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8011)
    ap.add_argument("--minutes", type=float, default=30)
    a = ap.parse_args()
    if a.cmd == "build":
        OUT.mkdir(parents=True, exist_ok=True)
        d = data()
        (OUT / "index.html").write_text(page(d), encoding="utf-8")
        print(f"{d['total_items']} problems in decks -> {(OUT / 'index.html').relative_to(ROOT)}")
    else:
        serve(a.host, a.port, a.minutes)
