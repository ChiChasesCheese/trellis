"""Tag one whole-answer card per problem with the classic lists it is on, so each list can be studied as a view.

    uv run python scripts/lc_lists.py            # dry run: what would be tagged
    uv run python scripts/lc_lists.py --apply    # replace the 榜单:: tags in Anki (AnkiConnect, desktop Anki running)

Tags are `榜单::Blind_75`, `榜单::NeetCode_150`, `榜单::Hot_100`, `榜单::Top_Interview_150` and `榜单::TikTok_近半年`. The card
tagged is fixed by the deck's layout alone: the problem's whole answer in its module deck (`tlc-tops-<slug>-0-whole`),
else its first other whole-answer card. It never depends on the learner's reviews; studying a copy as new is fine, and
progress across copies is the analysis' job (lc_analysis.py takes a problem's best card). Only tags change; fields, decks
and scheduling are untouched, and anki_refresh.py rewrites fields only, so the tags survive.
"""
from __future__ import annotations

import sys
from collections import defaultdict

from lc_data import call, classic_lists, problem_numbers, recent_slugs

TAGS = {"Blind 75": "Blind_75", "NeetCode 150": "NeetCode_150", "LeetCode Hot 100": "Hot_100", "Top Interview 150": "Top_Interview_150"}
PREFER = ("tlc-tops-{s}-0-whole", "tlc-{s}-0-whole", "tlc-core-{s}", "lca-{s}", "tlc-daily-{s}-0-whole")


def main() -> int:
    apply = "--apply" in sys.argv
    by_num = problem_numbers()
    members = {TAGS[k]: [by_num.get(n) for n in nums] for k, nums in classic_lists().items()}
    known = set(by_num.values())
    members["TikTok_近半年"] = sorted(s for s in set(recent_slugs("TikTok")) | set(recent_slugs("ByteDance")) if s in known)

    nids = call("findNotes", query='"deck:LeetCode Tops" OR "deck:1 今日计划" OR "deck:2 今日算法"')  # the daily decks borrow cards
    ident_note = {}
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            ident = next((t[4:] for t in n["tags"] if t.startswith("id::")), None)
            if ident:
                ident_note[ident] = n["noteId"]
    plan = defaultdict(list)
    for tag, slugs in members.items():
        missing = [s for s in slugs if s is None]
        for s in filter(None, slugs):
            note = next((ident_note[p.format(s=s)] for p in PREFER if p.format(s=s) in ident_note), None)
            if note is None:
                missing.append(s)
            else:
                plan[f"榜单::{tag}"].append(note)
        print(f"{tag}: {len(slugs)} problems, {len(plan[f'榜单::{tag}'])} cards, missing {missing}")
    if apply:
        old = call("findNotes", query="tag:榜单::*")
        for tag in plan:
            call("removeTags", notes=old, tags=tag)
        for tag, notes in plan.items():
            call("addTags", notes=notes, tags=tag)
        print(f"retagged (cleared {len(old)} notes first)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
