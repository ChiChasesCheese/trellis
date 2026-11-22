"""Aggregate reviewer verdicts (sources/local/audit/verdicts/*.json) and extrapolate them to whole decks.

    uv run python scripts/deck_verdicts.py            # table + sources/local/audit/verdicts.md
    uv run python scripts/deck_verdicts.py --tag      # also tag the example notes in Anki: audit::<verdict> (reversible)
    uv run python scripts/deck_verdicts.py --untag    # remove every audit::* tag again

Reviewers (see research/agents/deck-review.md) judge a random sample per domain; this script scales each rate by the
domain's note count from sources/local/audit/notes.jsonl, so "12 of 60 trivial" in a 900-note deck reads as ~180.
Nothing is deleted or suspended here: tagging only marks the reviewers' concrete examples so Chi can browse them
(Anki search `tag:audit::drop_trivial`).
"""
from __future__ import annotations

import collections
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "sources/local/audit"
KINDS = ("keep", "trim", "split", "merge", "drop_trivial", "drop_filler", "drop_stale", "fix")


def anki(action: str, **params):
    req = urllib.request.Request("http://127.0.0.1:8765", json.dumps({"action": action, "version": 6, "params": params}).encode())
    out = json.load(urllib.request.urlopen(req, timeout=120))
    if out["error"]:
        raise RuntimeError(out["error"])
    return out["result"]


def main() -> int:
    if "--untag" in sys.argv:
        ids = anki("findNotes", query="tag:audit::*")
        for kind in KINDS:
            anki("removeTags", notes=ids, tags=f"audit::{kind}")
        print("removed audit::* from", len(ids), "notes")
        return 0
    size: collections.Counter = collections.Counter()
    for line in (AUDIT / "notes.jsonl").open(encoding="utf-8"):
        size[json.loads(line)["domain"]] += 1
    verdicts: dict[str, dict] = {}
    for f in sorted((AUDIT / "verdicts").glob("*.json")):
        try:
            verdicts.update(json.loads(f.read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc:
            print(f"warning: {f.name}: {exc}", file=sys.stderr)
    rows, total = [], collections.Counter()
    for dom, v in sorted(verdicts.items(), key=lambda kv: -size.get(kv[0], 0)):
        n, sampled = size.get(dom, 0), max(1, int(v.get("sampled", 0)))
        est = {k: round(n * int(v.get(k, 0)) / sampled) for k in KINDS}
        drop = est["drop_trivial"] + est["drop_filler"] + est["drop_stale"]
        total.update({"notes": n, "drop": drop, "merge": est["merge"], "trim": est["trim"] + est["split"], "fix": est["fix"], "keep": est["keep"]})
        rows.append(f"| {dom} | {n} | {sampled} | {est['keep']} | {est['trim'] + est['split']} | {est['merge']} | {drop} "
                    f"({est['drop_trivial']}/{est['drop_filler']}/{est['drop_stale']}) | {est['fix']} | {v.get('recommendation', '')[:90]} |")
    head = ("| domain | notes | sampled | keep | trim/split | merge | drop (trivial/filler/stale) | fix | recommendation |\n"
            "|---|---|---|---|---|---|---|---|---|\n")
    tot = (f"| **total** | {total['notes']} | | {total['keep']} | {total['trim']} | {total['merge']} | {total['drop']} | {total['fix']} | |")
    issues = [f"- **{d}:** {i}" for d, v in verdicts.items() for i in v.get("norm_issues", [])]
    overlaps = [f"- **{d}:** {o}" for d, v in verdicts.items() for o in v.get("overlaps", [])]
    text = ("# Reviewer verdicts, extrapolated to whole decks\n\nEstimates = sample rate × deck size; a 60-note sample has a "
            "wide margin, so read them as orders of magnitude.\n\n" + head + "\n".join(rows) + "\n" + tot +
            "\n\n## Format and convention problems\n" + "\n".join(issues) + "\n\n## Overlaps\n" + "\n".join(overlaps) + "\n")
    (AUDIT / "verdicts.md").write_text(text, encoding="utf-8")
    print(text)
    if "--tag" in sys.argv:
        by_kind: dict[str, list[int]] = collections.defaultdict(list)
        for v in verdicts.values():
            for ex in v.get("examples", []):
                if ex.get("verdict") in KINDS and ex.get("verdict") != "keep":
                    by_kind[ex["verdict"]].append(int(ex["note"]))
        for kind, ids in by_kind.items():
            anki("addTags", notes=ids, tags=f"audit::{kind}")
            print(f"tagged {len(ids)} notes audit::{kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
