"""A company sprint deck: the cards one interview needs, from whatever domain holds them, in one daily deck.

    uv run python scripts/company_deck.py deal      # move the plan's cards in (idempotent; run again after the plan changes)
    uv run python scripts/company_deck.py status    # per part: cards, new, seen
    uv run python scripts/company_deck.py release   # the interview is over: every card goes back to its home deck
    uv run python scripts/company_deck.py rename "6 AI Infra SDET"   # same cards, scheduling and order, new deck name

The plan usually comes from a role track plus a company overlay (scripts/track_plan.py): to reuse the deck for the next
role, point the overlay at another track (or drop the company sections), rebuild the plan, `rename`, then `deal`.

Chi (2026-11-13): the cards stay in their own domains (the single source of truth); this deck only borrows
them, in the order the prep plan ranks them (80/20 by how likely and how central). Plan config `company`:
{"deck": "6 <company>", "plan": "<path to plan.json>", "new_per_day": 60}. plan.json is
[{"label": "01 公司与岗位::01 业务", "ids": ["<card id>", …]}, …]: one sub-deck per entry, named as given, so the
labels' numbers set the order the preset gathers new cards in (deck order). Cards keep their reviews here until `release`.

study_plan.py leaves these cards alone: they are read (so mastery is right) but never dealt into 今日计划 or the deep dive.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from anki_refresh import call  # noqa: E402

PLAN = ROOT / "sources/local/plan"
HOMES = PLAN / "company_homes.json"


def cfg() -> dict:
    return json.loads((PLAN / "config.json").read_text(encoding="utf-8")).get("company") or {}


def deck() -> str | None:
    return cfg().get("deck")


def homes() -> dict[str, str]:
    return json.loads(HOMES.read_text(encoding="utf-8")) if HOMES.exists() else {}


def _info(cids: list[int]) -> list[dict]:
    out = []
    for i in range(0, len(cids), 500):
        out += [c for c in call("cardsInfo", cards=cids[i:i + 500]) if c.get("note")]
    return out


def _ident(cards: list[dict]) -> dict[int, str]:
    nids = sorted({c["note"] for c in cards})
    by_note = {}
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            by_note[n["noteId"]] = next((t[4:] for t in n["tags"] if t.startswith("id::")), "")
    return {c["cardId"]: by_note.get(c["note"], "") for c in cards}


def reserved() -> set[str]:
    """Card idents in the company deck now: study_plan.py does not deal them elsewhere."""
    d = deck()
    if not d:
        return set()
    return set(_ident(_info(call("findCards", query=f'"deck:{d}"'))).values()) - {""}


def deal() -> int:
    import daily_extra
    c, d = cfg(), deck()
    plan = json.loads((ROOT / c["plan"]).read_text(encoding="utf-8"))
    want: dict[str, str] = {}  # ident -> sub-deck, first part wins
    for part in plan:  # labels carry their own numbers and may nest ("03 AI 从零开始::01 模型是什么")
        for i in part["ids"]:
            want.setdefault(i, f"{d}::{part['label']}")
    keys, tagged = list(want), []
    for k in range(0, len(keys), 300):  # one OR per id: Anki's SQL caps the expression depth at 1000
        tagged += call("findNotes", query=" OR ".join(f'"tag:id::{i}"' for i in keys[k:k + 300]))
    by_ident: dict[str, list[dict]] = defaultdict(list)
    cards = _info(call("findCards", query=f"nid:{','.join(map(str, tagged))}")) if tagged else []
    for cid, ident in _ident(cards).items():
        by_ident[ident].append(next(x for x in cards if x["cardId"] == cid))
    missing = [i for i in want if i not in by_ident]
    home, daily_home = homes(), daily_extra.homes()
    inside = _info(call("findCards", query=f'"deck:{d}"'))
    keep = {x["cardId"] for xs in by_ident.values() for x in xs}
    back = defaultdict(list)
    for x in inside:  # dropped from the plan: home again
        if x["cardId"] not in keep and str(x["cardId"]) in home:
            back[home.pop(str(x["cardId"]))].append(x["cardId"])
    for h, ids in back.items():
        call("changeDeck", cards=ids, deck=h)
    moves = defaultdict(list)
    for ident, xs in by_ident.items():
        for x in xs:
            if x["deckName"] != want[ident]:
                if not x["deckName"].startswith(d):
                    # borrowed today by a daily deck: its home is the daily deck's record, which this deck now owns
                    home[str(x["cardId"])] = daily_home.pop(str(x["cardId"]), x["deckName"]) if daily_extra.in_daily(x["deckName"]) else x["deckName"]
                moves[want[ident]].append(x["cardId"])
    for sub, ids in moves.items():
        call("changeDeck", cards=ids, deck=sub)
    HOMES.write_text(json.dumps(home, ensure_ascii=False, indent=0), encoding="utf-8")
    daily_extra.HOMES.write_text(json.dumps(daily_home, ensure_ascii=False, indent=0), encoding="utf-8")
    _preset(d, c.get("new_per_day", 60))
    empty = sorted((x for x in call("deckNames") if x.startswith(d + "::") and not call("findCards", query=f'"deck:{x}"')), key=len, reverse=True)
    if empty:
        call("deleteDecks", decks=empty, cardsToo=True)
    print(f"{d}: {len(keep)} cards in {len(plan)} parts, {sum(len(v) for v in moves.values())} moved in, "
          f"{sum(len(v) for v in back.values())} sent home, {len(missing)} plan ids not in Anki")
    if missing:
        print("  missing: " + " ".join(missing[:20]) + (" …" if len(missing) > 20 else ""))
    call("sync")
    return 0


def _preset(d: str, per_day: int) -> None:
    names = [x for x in call("deckNames") if x == d or x.startswith(d + "::")]
    title = d.split(" ", 1)[-1] + " 冲刺"
    known_f = PLAN / "presets.json"
    known = json.loads(known_f.read_text(encoding="utf-8")) if known_f.exists() else {}
    cid = known.get(title) or call("cloneDeckConfigId", name=title, cloneFrom=call("getDeckConfig", deck="系统设计")["id"])
    known[title] = cid
    known_f.write_text(json.dumps(known, ensure_ascii=False), encoding="utf-8")
    call("setDeckConfigId", decks=names, configId=cid)
    conf = call("getDeckConfig", deck=d)
    conf["new"]["perDay"], conf["rev"]["perDay"] = per_day, 9999
    conf["newGatherPriority"] = 0  # deck order: the plan's parts in turn
    call("saveDeckConfig", config=conf)


def status() -> int:
    d = deck()
    by = defaultdict(lambda: [0, 0])
    for x in _info(call("findCards", query=f'"deck:{d}"')):
        part = x["deckName"].split("::")[1] if "::" in x["deckName"] else "-"
        by[part][0] += 1
        by[part][1] += x["reps"] > 0
    for part in sorted(by):
        print(f"{part}\t{by[part][0]} cards\t{by[part][1]} seen")
    return 0


def rename(new: str) -> int:
    old = deck()
    moves = defaultdict(list)
    for x in _info(call("findCards", query=f'"deck:{old}"')):
        moves[new + x["deckName"][len(old):]].append(x["cardId"])
    for sub, ids in moves.items():
        call("changeDeck", cards=ids, deck=sub)
    f = PLAN / "config.json"
    c = json.loads(f.read_text(encoding="utf-8"))
    c["company"]["deck"] = new
    f.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    _preset(new, c["company"].get("new_per_day", 60))
    olds = sorted((x for x in call("deckNames") if x == old or x.startswith(old + "::")), key=len, reverse=True)
    call("deleteDecks", decks=[x for x in olds if not call("findCards", query=f'"deck:{x}"')], cardsToo=True)
    print(f"{old} -> {new}: {sum(len(v) for v in moves.values())} cards")
    call("sync")
    return 0


def release() -> int:
    home = homes()
    back = defaultdict(list)
    for x in _info(call("findCards", query=f'"deck:{deck()}"')):
        if str(x["cardId"]) in home:
            back[home.pop(str(x["cardId"]))].append(x["cardId"])
    for h, ids in back.items():
        call("changeDeck", cards=ids, deck=h)
    HOMES.write_text(json.dumps(home, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"sent home {sum(len(v) for v in back.values())}")
    call("sync")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["rename"] and len(a) == 2:
        sys.exit(rename(a[1]))
    sys.exit({"deal": deal, "status": status, "release": release}.get(a[0] if a else "", lambda: print(__doc__) or 2)())
