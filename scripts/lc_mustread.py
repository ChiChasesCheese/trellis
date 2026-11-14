"""Today's must-read LeetCode problems, as a tag on each problem's one card: `必读` (Chi, 2026-11-14: one card per problem).

    uv run python scripts/lc_mustread.py            # recompute and move the tag

The list is the dashboard's 必读 (scripts/lc_dashboard.py): problems whose estimated recall has decayed, that Chi keeps
forgetting, or that he just solved on LeetCode and has not reviewed, weighed by importance. The tag goes on the problem's
knowledge-tree card (`lct-<slug>`); a problem that leaves the list loses it. Study it as a view: `tag:必读` in the
browser, or a filtered deck on the phone. No copies, no deck. Run daily by the LeetCode Daily scheduled session.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import lc_dashboard as dash  # noqa: E402

TAG = "必读"


def main() -> int:
    d = dash.collect_anki()
    must = [m["s"] for m in d["must"] if (dash.SUBJECT["items"] / f"{m['s']}.md").exists()]
    old = dash.anki("findNotes", query=f"tag:{TAG}")
    if old:
        dash.anki("removeTags", notes=old, tags=TAG)
    found = []
    for i in range(0, len(must), 200):
        q = " OR ".join(f'"tag:id::lct-{s}"' for s in must[i:i + 200])
        found += dash.anki("findNotes", query=f"({q}) -\"deck:LeetCode Tops::99*\"")
    if found:
        dash.anki("addTags", notes=found, tags=TAG)
    print(f"{len(must)} must-read problems; tagged {len(found)} cards `{TAG}`")
    return 0

if __name__ == "__main__":
    sys.exit(main())
