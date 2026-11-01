"""Put today's must-read problems into Anki: deck `LeetCode Tops::00 必读（每天自动更新）`.

    uv run python scripts/lc_mustread.py            # recompute, rewrite the deck's stubs, push, drop what left the list

The list is the dashboard's 必读 (scripts/lc_dashboard.py): problems whose estimated recall has decayed, that Chi keeps
forgetting, or that he just solved on LeetCode and has not reviewed, weighed by importance. Each is a stub card over
the shared problem body, with the reasons in its header. A problem that leaves the list has its stub and its Anki note
removed (the copy only exists to surface it; its own decks keep the real history). Run daily by the LeetCode Daily
scheduled session; safe to run any time.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import lc_dashboard as dash  # noqa: E402

DOMAIN = "leetcode-mustread"
CARDS = ROOT / "vault/interviews/core/leetcode/mustread/cards"
SKELETON = ROOT / f"skeleton/{DOMAIN}.yaml"


def main() -> int:
    d = dash.collect_anki()
    row = {r["s"]: r for r in d["rows"]}
    must = [m for m in d["must"] if (dash.SUBJECT["items"] / f"{m['s']}.md").exists()]
    leaves, keep = [], set()
    CARDS.mkdir(parents=True, exist_ok=True)
    for m in must:
        r = row.get(m["s"], {"id": 0, "n": m["s"], "d": ""})
        name = (f"LC {r['id']} " if r["id"] else "") + r["n"]
        leaves.append({"id": f"today.{m['s']}", "title": name, "summary": "；".join(m["why"]) + "。"})
        meta = " · ".join(x for x in [r.get("d", "")] + m["why"] if x)
        f = CARDS / f"tlc-must-{m['s']}-0-whole.md"
        f.write_text(f"---\nid: tlc-must-{m['s']}-0-whole\nnode: today.{m['s']}\ntype: qa\n"
                     f"body: interviews/core/leetcode/problems/{m['s']}\nmeta: {json.dumps(meta, ensure_ascii=False)}\n---\n",
                     encoding="utf-8")
        keep.add(f.name)
    for f in CARDS.glob("*.md"):
        if f.name not in keep:
            f.unlink()
    head = "你已经 %d 天没复习了，先看这几道。" % d["gap"] if d["gap"] >= 3 else "按多久没看、平时忘得多不多、有多高频自动挑出的题。"
    sk = {"domain": DOMAIN, "title": "LeetCode 必读", "deck": "LeetCode Tops::00 必读（每天自动更新）", "lang": "zh",
          "vault": "interviews/core/leetcode/mustread", "examples_from": "interviews/core/leetcode/problems",
          "study": {"order": "core-first", "mix": "new-first", "new_per_day": 30, "reviews_per_day": 200},
          "nodes": [{"id": "today", "order": 1, "core": True, "title": "今天必读", "summary": head, "children": leaves}]}
    SKELETON.write_text("# Rewritten by scripts/lc_mustread.py every day; do not edit.\n"
                        + yaml.safe_dump(sk, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    uv = shutil.which("uv") or "uv"
    subprocess.run([uv, "run", "trellis", "--domain", DOMAIN, "anki-push"], cwd=ROOT, check=True)
    # remove the copies of problems that left the list
    current = {f"{DOMAIN}::today::{m['s']}" for m in must}
    stale = [n["noteId"] for n in dash.anki("notesInfo", notes=dash.anki("findNotes", query=f"tag:{DOMAIN}::*"))
             if not any(t in current for t in n["tags"])]
    if stale:
        dash.anki("deleteNotes", notes=stale)
    print(f"{len(must)} must-read problems; {len(stale)} dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
