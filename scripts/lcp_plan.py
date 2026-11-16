"""The LeetCode Project view: the deck `8 LC Project`, re-dealt from the knowledge tree and Chi's graded attempts.

    uv run python scripts/lcp_plan.py              # write the plan and deal it (company_deck.py deal)
    uv run python scripts/lcp_plan.py --dry-run    # print the parts, write nothing

Chi (2026-11-16): the projects are summarised on the low-level-design tree (branch `lcproject`, home deck
低层设计（LLD）::28 LeetCode Project（实战项目）), and studied through a view that borrows them, the way a sprint deck
does (scripts/company_deck.py, config `company`). He answers every project card before turning it; the daily run
grades the answer (docs/card-notes.md, answer cards) into sources/local/lc-project/attempts.jsonl.

The plan is the reinforcement loop made concrete:
- `00 补弱`: every card of the leaves his recent attempts missed (the most missed first), so the next cards he meets
  are the knowledge his answers lacked;
- then one part per project in the skeleton's order (the study order): `1 先修`, the first cards of the leaves the
  project's points.json names, and `2 作答`, the project's answer cards in step order;
- `3 第二次练`, for an exam point only that project tests: every point is practised at least twice (Chi,
  2026-11-16), so its second practice comes from the bank or another domain (lc-project/second_practice.json).
A card already borrowed by an earlier sprint deck stays there (company_deck.py: the first plan naming a card wins).
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trellis.project import load_project  # noqa: E402

HOME = ROOT / "sources/local/lc-project"
PLAN = HOME / "plan.json"
ATTEMPTS = HOME / "attempts.jsonl"
PROBLEMS = ROOT / "vault/domains/low-level-design/problems"
SECOND = ROOT / "research/domains/low-level-design/lc-project/second_practice.json"
PREREQ_PER_LEAF = 3   # 先修: the first cards of each leaf a project stands on
RECENT = 60           # attempts that count towards 补弱
WEAK_SCORE = 0.75     # an attempt below this sends its missed leaves to 补弱


def ordered(cards) -> list[str]:
    return [c.id for c in sorted(cards, key=lambda c: (c.step is None, c.step or 0, c.id))]


def weak_leaves() -> list[str]:
    if not ATTEMPTS.exists():
        return []
    rows = [json.loads(line) for line in ATTEMPTS.read_text(encoding="utf-8").splitlines() if line.strip()][-RECENT:]
    misses = Counter(leaf for r in rows if r.get("score", 1) < WEAK_SCORE for leaf in r.get("leaves", []))
    return [leaf for leaf, _ in misses.most_common()]


def plan() -> list[dict]:
    project = load_project(ROOT, "low-level-design")
    by_leaf: dict[str, list] = {}
    for c in project.cards:
        by_leaf.setdefault(c.node, []).append(c)
    parts, seen = [], set()

    def take(ids: list[str]) -> list[str]:
        out = [i for i in ids if i not in seen]
        seen.update(out)
        return out

    weak = [i for leaf in weak_leaves() for i in ordered(by_leaf.get(leaf, []))]
    if ids := take(weak):
        parts.append({"label": "00 补弱", "ids": ids})
    second = json.loads(SECOND.read_text(encoding="utf-8")) if SECOND.exists() else {}
    leaves = [l for l in project.skeleton.leaves() if l.id.startswith("lcproject.")]
    for n, leaf in enumerate(leaves, 1):  # numbered by the leaf's place in the study order, so labels never shift
        if not by_leaf.get(leaf.id):
            continue
        slug = leaf.id.split(".", 1)[1]
        points = PROBLEMS / slug / "points.json"
        need = [lid for p in json.loads(points.read_text(encoding="utf-8")) for lid in p.get("leaves", [])] if points.exists() else []
        need = list(dict.fromkeys(need))
        prereq = take([i for lid in need for i in ordered(by_leaf.get(lid, []))[:PREREQ_PER_LEAF]])
        own = take(ordered(by_leaf[leaf.id]))
        title = leaf.title.split("（")[0]
        if prereq:
            parts.append({"label": f"{n:02d} {title}::1 先修", "ids": prereq})
        parts.append({"label": f"{n:02d} {title}::2 作答", "ids": own})
        extra = second.get(slug.removeprefix("lcp-"), {})
        if ids := take([i for lid in extra.get("leaves", []) for i in ordered(by_leaf.get(lid, []))] + extra.get("ids", [])):
            parts.append({"label": f"{n:02d} {title}::3 第二次练", "ids": ids})
    return parts


def main() -> int:
    parts = plan()
    for p in parts:
        print(f"{p['label']}: {len(p['ids'])}")
    if "--dry-run" in sys.argv:
        return 0
    HOME.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(parts, ensure_ascii=False, indent=1), encoding="utf-8")
    return subprocess.run(["uv", "run", "python", "scripts/company_deck.py", "--deck", "8 LC Project", "deal"], cwd=ROOT).returncode


if __name__ == "__main__":
    sys.exit(main())
