"""Choose the LeetCode Tops problem set by the 80/20 rule and file each problem under a topic branch.

    uv run python research/leetcode-tops/select.py      # -> research/leetcode-tops/selection.json

Chi (2026-10-31) picked: the 300 most frequent problems across every company's LeetCode tag (liquidslr repo, 6-month
frequency + 0.3 x all-time, summed over ~470 companies) plus every problem on at least two of Blind 75 / NeetCode 150 /
LeetCode Hot 100 / Top Interview 150 / LeetCode 75; SQL problems excluded; every problem of the old deck stays (only add, never drop). That is ~312 problems covering ~58% of all
company-tag frequency, against 49% for the plain union of the lists (300 problems).
Branch: the topic branch the old deck used for the problem, else the classic-lists knowledge point mapped to a branch,
else empty (filled by an agent).
"""
from __future__ import annotations

import csv
import json
import os
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "sources/local/lq-all/repo"
OLD_MAP = Path.home() / "Code/trellis/vault/interviews/core/leetcode/tops/map"
BRANCHES = ["arrays-hashing", "two-pointers", "sliding-window", "stack", "binary-search", "linked-list", "trees", "tries",
            "heap-priority-queue", "backtracking", "graphs", "dp-1d", "dp-2d", "greedy", "intervals", "math-geometry",
            "bit-manipulation"]
POINT_TO_BRANCH = {"hashing": "arrays-hashing", "prefix-sum": "arrays-hashing", "two-pointers": "two-pointers",
                   "sliding-window": "sliding-window", "stack": "stack", "monotonic-stack": "stack",
                   "binary-search": "binary-search", "linked-list": "linked-list", "tree-dfs": "trees", "tree-bfs-bst": "trees",
                   "heap-patterns": "heap-priority-queue", "intervals-sweep": "intervals", "graph-traversal": "graphs",
                   "topo-sort": "graphs", "union-find": "graphs", "shortest-path": "graphs", "backtracking": "backtracking",
                   "trie": "tries", "greedy": "greedy", "dp-linear": "dp-1d", "dp-knapsack": "dp-1d", "dp-grid-string": "dp-2d",
                   "matrix": "math-geometry", "string-parsing": "stack"}
SQL = re.compile(r"salary|employee|customer|department|duplicate-emails|rising-temperature|combine-two-tables|rank-scores|"
                 r"game-play|trips-and-users|human-traffic|students|managers|sellers|queries-quality|confirmation-rate|"
                 r"article-views|actors|tweets|movie-rating|product-sales|followers|recyclable|big-countries|fix-names|"
                 r"patients|bank-account|triangle-judgement|biggest-single|exchange-seats|investments-in-2016|"
                 r"restaurant-growth|friend-requests|average-selling|monthly-transactions|immediate-food|daily-leads|"
                 r"average-time-of-process|consecutive-numbers$|second-highest|nth-highest|delete-duplicate-emails")


def scores() -> tuple[dict, dict]:
    score, title = defaultdict(float), {}
    for d in os.listdir(REPO):
        for fn, w in (("3. Six Months.csv", 1.0), ("5. All.csv", 0.3)):
            f = REPO / d / fn
            if not f.exists():
                continue
            for r in csv.DictReader(open(f, encoding="utf-8", errors="replace")):
                m = re.search(r"/problems/([^/]+)", r.get("Link", ""))
                if m:
                    score[m.group(1)] += w * float(r.get("Frequency") or 0) / 100
                    title[m.group(1)] = (r["Title"], r["Difficulty"].title())
    return score, title


def main() -> None:
    score, title = scores()
    meta = json.loads((ROOT / "research/companies/tiktok/catalog/lc_meta.json").read_text(encoding="utf-8"))
    classic = json.loads((ROOT / "research/classic-lists/index.json").read_text(encoding="utf-8"))
    points = json.loads((ROOT / "research/classic-lists/points.json").read_text(encoding="utf-8"))
    other = json.loads((ROOT / "research/companies/tiktok/catalog/other_lists.json").read_text(encoding="utf-8"))
    slug_of = {int(k): v["slug"] for k, v in meta.items()} | {int(k): v["slug"] for k, v in classic.items()}
    lists = {"Blind 75": other["Blind 75"], "NeetCode 150": other["NeetCode 150"], "Hot 100": other["LeetCode Hot 100"],
             "Top Interview 150": other["Top Interview 150"],
             "LeetCode 75": [int(k) for k, v in classic.items() if "LeetCode 75" in v["lists"]]}
    on = defaultdict(list)
    for name, ids in lists.items():
        for n in ids:
            on[slug_of.get(int(n), str(n))].append(name)
    old = {}
    for f in OLD_MAP.glob("*.*.md"):
        b, s = f.stem.split(".", 1)
        if b in BRANCHES:
            old[s] = b
    ranked = [s for s in sorted(score, key=lambda s: -score[s]) if not SQL.search(s)]
    chosen = set(ranked[:300]) | {s for s, names in on.items() if len(names) >= 2}
    chosen |= set(old)  # Chi: only add, never drop — every problem of the old deck stays
    total = sum(score.values())
    by_slug_point = {v["slug"]: points.get(k, "") for k, v in classic.items()}
    prev = {p["slug"]: p for p in json.loads((ROOT / "research/leetcode-tops/selection.json").read_text(encoding="utf-8"))} \
        if (ROOT / "research/leetcode-tops/selection.json").exists() else {}
    out = []
    for s in sorted(chosen, key=lambda s: -score.get(s, 0)):
        out.append({"slug": s, "title": title.get(s, ("", ""))[0], "difficulty": title.get(s, ("", ""))[1],
                    "score": round(score.get(s, 0), 2), "rank": ranked.index(s) + 1 if s in ranked else None,
                    "lists": on.get(s, []), "old_branch": old.get(s, ""),
                    "branch": old.get(s) or POINT_TO_BRANCH.get(by_slug_point.get(s, ""), "") or prev.get(s, {}).get("branch", "")})
    (ROOT / "research/leetcode-tops/selection.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "problems; mass", round(100 * sum(score.get(p["slug"], 0) for p in out) / total, 1), "%;",
          sum(1 for p in out if p["old_branch"]), "already in the old deck;", sum(1 for p in out if not p["branch"]), "without a branch;",
          len([s for s in old if s not in chosen]), "old-deck problems dropped")


if __name__ == "__main__":
    main()
