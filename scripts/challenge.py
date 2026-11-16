"""Challenge cards: withheld until the leaf is learnt, and the transfer rate they measure.

    uv run python scripts/challenge.py            # what the gate would do, and the rate; nothing written to Anki
    uv run python scripts/challenge.py --apply    # suspend / release (study_plan.py daily does this)

A leaf's ordinary cards demonstrate: question, answer, repeat. A challenge card (tag 挑战, last step of its leaf)
gives a situation the leaf's cards did not show, a list of grading points and a folded reference answer. Showing it
before the leaf is learnt would turn it into one more demonstration, so the gate keeps it suspended until every other
card of its leaf has graduated from the learning steps, and releases it on the next daily run.

Only a challenge card never answered is touched. A card the gate suspended carries the tag 挑战::待放出, and only a
card with that tag is released: one suspended by hand stays suspended.

The transfer rate is the share of challenge cards answered Good or Easy the first time. It is shown next to the
retention of the same leaves' ordinary cards (review answers that were not Again). High retention with a low transfer
rate means the wording was memorised, not the mechanism.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from anki_refresh import call  # noqa: E402

TAG = "挑战"
HELD = "挑战::待放出"
OUT = ROOT / "sources/local/plan/challenge.json"


def domains() -> set[str]:
    out = set()
    for f in (ROOT / "skeleton").glob("*.yaml"):
        m = re.search(r"^domain:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
        if m:
            out.add(m.group(1))
    return out


def leaf_tag(tags: list[str], known: set[str]) -> str | None:
    """The tag that names the card's leaf: `<domain>::<node path>`."""
    return next((t for t in tags if t.split("::")[0] in known and "::" in t), None)


def gate(dry: bool = True) -> dict:
    """Suspend the challenge cards whose leaf is not learnt yet, release the ones whose leaf is. Returns the counts
    and the transfer rate."""
    cards = call("cardsInfo", cards=call("findCards", query=f"tag:{TAG}"))
    notes = {n["noteId"]: n["tags"] for n in call("notesInfo", notes=sorted({c["note"] for c in cards}))}
    known = domains()
    by_leaf: dict[str, list[dict]] = {}
    for c in cards:
        leaf = leaf_tag(notes.get(c["note"], []), known)
        if leaf:
            by_leaf.setdefault(leaf, []).append(c)
    hold, free, drop_tag, others = [], [], [], []
    for leaf, mine in by_leaf.items():
        rest = call("cardsInfo", cards=call("findCards", query=f'"tag:{leaf}" -tag:{TAG}'))
        others += [c["cardId"] for c in rest if c["reps"]]
        learnt = all(c["type"] in (2, 3) for c in rest)  # review or relearning: past the learning steps once
        for c in mine:
            held = HELD in notes[c["note"]]
            if c["reps"]:  # answered: it is the learner's card now
                if held:
                    drop_tag.append(c["note"])
            elif learnt and held:
                free.append(c)
            elif not learnt and c["queue"] != -1:
                hold.append(c)
    if not dry:
        if hold:
            call("suspend", cards=[c["cardId"] for c in hold])
            call("addTags", notes=[c["note"] for c in hold], tags=HELD)
        if free:
            call("unsuspend", cards=[c["cardId"] for c in free])
        if free or drop_tag:
            call("removeTags", notes=[c["note"] for c in free] + drop_tag, tags=HELD)
    answered = [c["cardId"] for c in cards if c["reps"]]
    logs = call("getReviewsOfCards", cards=answered) if answered else {}
    first = [min(v, key=lambda r: r["id"])["ease"] for v in logs.values() if v]
    reviews = [r["ease"] for v in (call("getReviewsOfCards", cards=others) if others else {}).values() for r in v if r["type"] == 1]
    out = {"total": len(cards), "leaves": len(by_leaf), "held": sum(1 for c in cards if not c["reps"] and c["queue"] == -1) + len(hold) - len(free),
           "to_hold": len(hold), "released": len(free), "answered": len(first), "passed": sum(1 for e in first if e >= 3),
           "retention": (sum(1 for e in reviews if e > 1) / len(reviews)) if reviews else None}
    out["rate"] = out["passed"] / out["answered"] if out["answered"] else None
    if not dry:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def line(s: dict) -> str:
    """One line for the daily report card."""
    head = f"挑战卡 {s['total']} 张：今天放出 {s['released']}，待放出 {s['held']}"
    if s["rate"] is None:
        return head + "；还没有答过，迁移率暂无"
    keep = f"，同叶子复习保持率 {s['retention']:.0%}" if s["retention"] is not None else ""
    return head + f"；迁移率 {s['passed']}/{s['answered']} = {s['rate']:.0%}（第一次就答对的比例{keep}）"


def main() -> int:
    s = gate(dry="--apply" not in sys.argv)
    print(line(s))
    print(f"leaves {s['leaves']} · to suspend {s['to_hold']} · to release {s['released']}" + ("" if "--apply" in sys.argv else " (dry run)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
