"""Put a sprint deck's new cards in the plan's order (Anki deals new cards by position inside a sub-deck).

    uv run --no-project --with anki==26.9.3 python -I scripts/reposition_new.py <collection.anki2> <plan.json> "<deck>"

Run with desktop Anki closed and a backup taken; then reopen and sync. AnkiConnect cannot write positions. A
reposition alone syncs normally; only schema changes force a full sync.
"""
import json
import sys

from anki.collection import Collection

col = Collection(sys.argv[1])
plan = json.load(open(sys.argv[2], encoding="utf-8"))
rank: dict[str, int] = {}
for part in plan:
    for ident in part["ids"]:
        rank.setdefault(ident, len(rank))
rows = []
for cid in col.find_cards(f'"deck:{sys.argv[3]}" is:new'):
    card = col.get_card(cid)
    ident = next((t[4:] for t in card.note().tags if t.startswith("id::")), "")
    rows.append((rank.get(ident, 10**9), card.ord, card.due, cid))
rows.sort()
if rows:
    col.sched.reposition_new_cards([r[3] for r in rows], starting_from=min(r[2] for r in rows), step_size=1,
                                   randomize=False, shift_existing=False)
col.close()
print(f"repositioned {len(rows)}")
