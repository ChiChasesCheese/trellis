"""Tag one whole-answer card per problem with the classic lists it is on, so each list can be studied as a view.

    uv run python scripts/lc_lists.py            # dry run: what would be tagged
    uv run python scripts/lc_lists.py --apply    # add the tags in Anki (AnkiConnect, desktop Anki running)

Tags are `榜单::Blind_75`, `榜单::NeetCode_150`, `榜单::Hot_100`, `榜单::Top_Interview_150` and `榜单::TikTok_近半年`. The card
tagged is the problem's whole-answer card the learner has reviewed most (so a list view continues an existing schedule
instead of dealing a duplicate as new); with no reviews, the one in its module deck (`tlc-tops-<slug>-0-whole`). A filtered
deck over a tag therefore holds exactly one card per problem. Only tags are added; fields, decks and scheduling are untouched,
and anki_refresh.py rewrites fields only, so the tags survive. Lists by problem number come from
research/companies/tiktok/catalog/other_lists.json (neetcode-gh .problemSiteData.json and LeetCode study plans).
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict

sys.path.insert(0, __import__("os").path.dirname(__file__))
import lc_analysis as L  # noqa: E402

LISTS = {"Blind 75": "Blind_75", "NeetCode 150": "NeetCode_150", "LeetCode Hot 100": "Hot_100", "Top Interview 150": "Top_Interview_150"}
PREFER = ("tlc-tops-{s}-0-whole", "tlc-{s}-0-whole", "tlc-core-{s}", "lca-{s}", "tlc-daily-{s}-0-whole")


def main() -> int:
    apply = "--apply" in sys.argv
    rows = {json.loads(line)["slug"]: json.loads(line) for line in (L.OUT / "sections.jsonl").read_text(encoding="utf-8").splitlines()}
    by_num = {}
    for slug, r in rows.items():
        m = __import__("re").match(r"LC (\d+)", r["title"])
        if m:
            by_num[int(m.group(1))] = slug
    other = json.loads(L.OTHER.read_text(encoding="utf-8"))
    members = {tag: [by_num.get(n) for n in other[key]] for key, tag in LISTS.items()}
    gh = L.github_frequency()
    members["TikTok_近半年"] = sorted(s for s, o in gh.items() if o["tiktok_recent"] and s in rows)

    nids = L.call("findNotes", query='"deck:LeetCode Tops" OR "deck:LeetCode"')
    ident_note, reps = {}, defaultdict(int)
    for i in range(0, len(nids), 500):
        for n in L.call("notesInfo", notes=nids[i:i + 500]):
            ident = next((t[4:] for t in n["tags"] if t.startswith("id::")), None)
            if ident:
                ident_note[ident] = n["noteId"]
    cids = L.call("findCards", query='"deck:LeetCode Tops" OR "deck:LeetCode"')
    for i in range(0, len(cids), 500):
        for c in L.call("cardsInfo", cards=cids[i:i + 500]):
            if c["queue"] != -1:  # a suspended card cannot be studied from a filtered deck
                reps[c["note"]] += c["reps"] + 1
    plan = defaultdict(list)
    for tag, slugs in members.items():
        missing = [s for s in slugs if s is None]
        for s in slugs:
            if s is None:
                continue
            cands = [ident_note[p.format(s=s)] for p in PREFER if ident_note.get(p.format(s=s)) in reps]
            note = max(cands, key=lambda n: (reps[n], -cands.index(n))) if cands else None
            if note is None:
                missing.append(s)
            else:
                plan[f"榜单::{tag}"].append(note)
        print(f"{tag}: {len(slugs)} problems, {len(plan[f'榜单::{tag}'])} cards to tag, missing {missing}")
    if apply:
        for tag, notes in plan.items():
            L.call("addTags", notes=notes, tags=tag)
        print("tagged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
