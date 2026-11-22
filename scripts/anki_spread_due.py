"""Clear a review backlog without resetting progress: spread overdue cards evenly over the next N days. Reversible.

    uv run python scripts/anki_spread_due.py              # report what is overdue and how it would be spread
    uv run python scripts/anki_spread_due.py --days 30 --apply
    uv run python scripts/anki_spread_due.py --only-top '📦 其他' --start 31 --days 60 --apply   # one deck tree, later window
    uv run python scripts/anki_spread_due.py --skip-top '📦 其他' --days 30 --apply              # everything else
    uv run python scripts/anki_spread_due.py --restore sources/local/plan/overdue-snapshot-<date>.json --apply

What counts as backlog: review cards due before today, and learning cards stuck for more than a day (answered once,
never brought back). Cards due today are today's work and stay. Suspended cards are left alone.
- A review card keeps its interval; only its due date moves to one of the next N days.
- A stuck learning card becomes a review card due on its new day (interval = days from today), which is what
  "see it again on that day" means for a card that never finished its steps.
Each day gets the same share of every deck (round-robin by deck). Before anything changes, every card's scheduling
(type, queue, due, interval, ease, steps left) is saved to sources/local/plan/overdue-snapshot-<date>.json.
"""
from __future__ import annotations

import collections
import datetime
import json
import os
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTION = Path(os.path.expanduser("~/Library/Application Support/Anki2/User 1/collection.anki2"))


def anki(action: str, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", json.dumps({"action": action, "version": 6, "params": params}).encode())
    for _ in range(60):
        out = json.load(urllib.request.urlopen(req, timeout=300))
        if out["error"] and "lifecycle" in str(out["error"]):
            time.sleep(2)
            continue
        if out["error"]:
            raise RuntimeError(out["error"])
        return out["result"]
    raise RuntimeError("Anki stayed busy for two minutes")


def backlog() -> tuple[list[dict], int]:
    db = sqlite3.connect(f"file:{COLLECTION}?mode=ro", uri=True)
    db.create_collation("unicase", lambda a, b: (a.lower() > b.lower()) - (a.lower() < b.lower()))
    crt = db.execute("select crt from col").fetchone()[0]
    now = time.time()
    today = int((now - crt) // 86400)
    decks = {i: n.replace("\x1f", "::") for i, n in db.execute("select id, name from decks")}
    rows = db.execute("select id, did, type, queue, due, ivl, factor, left from cards where "
                      "(queue = 2 and due < ?) or (queue = 3 and due < ?) or (queue = 1 and due < ?)",
                      (today, today, now - 86400)).fetchall()
    keys = ("id", "did", "type", "queue", "due", "ivl", "factor", "left")
    cards = [dict(zip(keys, r), deck=decks.get(r[1], "?")) for r in rows]
    return cards, today


def main() -> int:
    args = sys.argv[1:]
    apply = "--apply" in args
    if "--restore" in args:
        snap = json.loads(Path(args[args.index("--restore") + 1]).read_text(encoding="utf-8"))
        print(f"restore scheduling of {len(snap['cards'])} cards from {snap['date']}")
        if apply:
            for c in snap["cards"]:
                anki("setSpecificValueOfCard", card=c["id"], keys=["type", "queue", "due", "ivl", "left"],
                     newValues=[c["type"], c["queue"], c["due"], c["ivl"], c["left"]], warning_check=True)
            anki("sync")
        return 0
    days = int(args[args.index("--days") + 1]) if "--days" in args else 30
    start = int(args[args.index("--start") + 1]) if "--start" in args else 1
    cards, _ = backlog()
    if "--only-top" in args:
        cards = [c for c in cards if c["deck"].split("::")[0] == args[args.index("--only-top") + 1]]
    if "--skip-top" in args:
        cards = [c for c in cards if c["deck"].split("::")[0] != args[args.index("--skip-top") + 1]]
    review = [c for c in cards if c["queue"] == 2]
    stuck = [c for c in cards if c["queue"] != 2]
    by_top = collections.Counter(c["deck"].split("::")[0] for c in cards)
    print(f"backlog: {len(review)} overdue reviews + {len(stuck)} stuck learning cards = {len(cards)}")
    print("  " + ", ".join(f"{d} {n}" for d, n in by_top.most_common(8)))
    # round-robin by deck so every day carries the same mix
    queues: dict[str, list[dict]] = collections.defaultdict(list)
    for c in sorted(cards, key=lambda c: c["id"]):
        queues[c["deck"].split("::")[0]].append(c)
    order: list[dict] = []
    while any(queues.values()):
        for top in sorted(queues):
            if queues[top]:
                order.append(queues[top].pop())
    slots: dict[int, list[int]] = collections.defaultdict(list)
    for i, c in enumerate(order):
        slots[start + i % days].append(c["id"])
    print(f"spread over days {start}–{start + days - 1}: {len(order) // days}–{-(-len(order) // days)} cards a day, on top of what is already scheduled")
    if not apply or not cards:
        return 0
    snap = ROOT / f"sources/local/plan/overdue-snapshot-{datetime.date.today()}.json"
    saved = json.loads(snap.read_text(encoding="utf-8")) if snap.exists() else {"date": str(datetime.date.today()), "cards": []}
    have = {c["id"] for c in saved["cards"]}
    saved["cards"] += [c for c in cards if c["id"] not in have]   # a second run the same day adds to the snapshot
    snap.write_text(json.dumps(saved, ensure_ascii=False), encoding="utf-8")
    for day, ids in sorted(slots.items()):
        anki("setDueDate", cards=ids, days=str(day))
    anki("sync")
    print("done; snapshot:", snap.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
