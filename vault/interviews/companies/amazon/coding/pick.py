#!/usr/bin/env python3
"""Pick the sprint problem list from the generated Amazon LeetCode tag list.

Input : vault/interviews/core/leetcode/companies/amazon.md  (generated, read-only)
Rule  : A tier  AND  recent (近) = ✓  AND  both sources (双源) = ✓  AND  has an LC number
        -> classify each row into one of 11 patterns (TAG_RULES, with OVERRIDE for ambiguous ones)
        -> drop DB / JS-only problems (EXCLUDE)
        -> dedupe by FAMILY (variants of one idea: keep the highest-frequency member)
        -> rank by frequency, keep the top QUOTA[pattern] per pattern
Senior bar (Chi, 2026-10-15): after the quota pass, every pattern is topped up with A-tier Hard problems
        until it has TARGET_HARD of them (when the tag list has such Hards): HARD_PREFER order first, then frequency.
Output: a markdown table on stdout (this is pasted into top_list.md).
Run   : python3 -I coding/pick.py [path-to-amazon.md]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = HERE.parents[2] / "core" / "leetcode" / "companies" / "amazon.md"

# (slug, title, quota). Order == lecture order == plan order.
PATTERNS = [
    ("01_hash_map_counting", "Hash map counting / prefix sum", 4),
    ("02_two_pointers_sliding_window", "Two pointers / sliding window", 4),
    ("03_intervals", "Intervals (sort + sweep)", 4),
    ("04_stack_monotonic_stack", "Stack / monotonic stack", 4),
    ("05_heap_top_k", "Heap / top-k", 4),
    ("06_graph_bfs_dfs_topo", "BFS / DFS on grids & graphs, topological sort", 4),
    ("07_binary_search_on_answer", "Binary search (incl. on the answer)", 3),
    ("08_linked_list", "Linked list", 4),
    ("09_trees_lca", "Trees / LCA", 4),
    ("10_dp_1d_2d", "Dynamic programming 1D / 2D", 5),
    ("11_design_lru_lfu_iterators", "Design: LRU / LFU / iterators", 3),
]
QUOTA = {s: q for s, _, q in PATTERNS}
TITLE = {s: t for s, t, _ in PATTERNS}

H, SW, IV, ST, HP, GR, BS, LL, TR, DP, DS = (p[0] for p in PATTERNS)

# Ordered: first rule whose tag is present wins.
TAG_RULES = [
    ("Design", DS),
    ("Monotonic Stack", ST),
    ("Stack", ST),
    ("Heap (Priority Queue)", HP),
    ("Topological Sort", GR),
    ("Union-Find", GR),
    ("Graph Theory", GR),
    ("Breadth-First Search", GR),
    ("Binary Search", BS),
    ("Linked List", LL),
    ("Binary Tree", TR),
    ("Tree", TR),
    ("Sliding Window", SW),
    ("Two Pointers", SW),
    ("Dynamic Programming", DP),
    ("Prefix Sum", H),
    ("Hash Table", H),
    ("Depth-First Search", GR),
]

# Hand fixes where tags point at the wrong teaching home.
OVERRIDE = {
    42: SW,    # Trapping Rain Water: two-pointer O(1) space is the main solution
    295: HP,   # Find Median from Data Stream: two heaps, not "design"
    155: ST,   # Min Stack: stack with a parallel min stack
    380: DS,   # Insert Delete GetRandom O(1)
    56: IV, 253: IV, 57: IV, 435: IV, 252: IV, 986: IV, 452: IV, 759: IV, 1235: IV,
    23: HP,    # Merge k Sorted Lists: heap of list heads
    199: TR, 102: TR, 103: TR, 297: TR,   # tree BFS/serialize live with trees
    863: TR,
    33: BS, 4: BS, 162: BS, 153: BS,
    167: SW, 11: SW, 15: SW, 18: SW, 16: SW,
    128: H, 49: H, 560: H, 1: H, 238: H,
    300: DP, 53: DP, 121: DP,
    207: GR, 210: GR, 200: GR, 994: GR, 127: GR, 733: GR, 79: GR,
    322: DP,
    875: BS, 1011: BS, 410: BS,
    215: HP, 347: HP, 973: HP, 621: HP, 767: HP,
    239: ST,   # Sliding Window Maximum: monotonic deque, taught next to the monotonic stack
    5: DP,     # Longest Palindromic Substring: 2D table (expand-around-center noted as alternative)
    22: None,  # backtracking: not one of the 11 patterns (listed under "not covered")
    55: None, 45: None,  # greedy: not covered
    37: None, 51: None, 212: None, 126: None,  # backtracking-heavy Hards: not covered
    987: TR,   # vertical-order traversal lives with trees
}

# Ties on frequency are broken by this teaching order (earlier wins), then by LC number.
PREFER = [739, 84, 460, 380, 206, 1011, 994]

# Hard add-ons (senior bar): preferred order, then plain frequency (>= 50).
TARGET_HARD = 2
HARD_PREFER = [41, 76, 1235, 269, 410, 25, 10, 312, 588]

# Variants of one idea. Only the highest-frequency member survives.
FAMILIES = {
    "kSum": {15, 16, 18, 167},
    "next-greater": {496, 503, 739},
    "stock": {121, 122},
    "jump": {55, 45},
    "kth-largest": {215, 973},
    "tree-bfs-levels": {102, 103, 199},
    "grid-flood": {200, 733},
    "course-schedule": {207, 210},
    "lca": {236, 235, 1650},
    "bs-rotated": {33, 153, 34},
    "bs-answer": {410},
    "sliding-count": {3, 424, 904, 1004, 438},
    "path-sum-dp-grid": {62, 64},
    "fib-like": {70, 198, 509},
    "linked-list-reverse": {25},
    "interval-trivial": {57, 252, 986, 452},
    "lru-like": {432},
    "anagram": {49, 242},
    "count-based-hash": {217, 169, 387},
}

EXCLUDE_TAGS = {"Database"}
EXCLUDE_NUMS = {2667}  # JavaScript-only 30-days problem

ROW = re.compile(
    r"^\| (\d+|) \| \[(.*?)\]\((.*?)\) \| (\w+) \| (\d+) \| (.*?) \| (.*?) \| (.*?) \| .*\|$"
)


def parse(path):
    tier = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            tier = line[3]
            continue
        m = ROW.match(line)
        if not m or not m.group(1):
            continue
        num, name, url, diff, freq, recent, both, tags = m.groups()
        yield dict(num=int(num), name=name, url=url, diff=diff, freq=int(freq),
                   recent=recent.strip() == "✓", both=both.strip() == "✓",
                   tags=[t.strip() for t in tags.split(",") if t.strip()], tier=tier)


def classify(r):
    if r["num"] in OVERRIDE:
        return OVERRIDE[r["num"]]  # may be None = deliberately not covered
    for tag, slug in TAG_RULES:
        if tag in r["tags"]:
            return slug
    return None


def family_of(num):
    for fam, members in FAMILIES.items():
        if num in members:
            return fam
    return f"solo-{num}"


def rank(r):
    pref = PREFER.index(r["num"]) if r["num"] in PREFER else len(PREFER)
    return (-r["freq"], pref, r["num"])


def pick(rows):
    cands = [r for r in rows
             if r["tier"] == "A" and r["recent"] and r["both"]
             and not (set(r["tags"]) & EXCLUDE_TAGS) and r["num"] not in EXCLUDE_NUMS]
    stats = {"A-tier rows with LC number": len([r for r in rows if r["tier"] == "A"]),
             "recent+both": len(cands)}
    for r in cands:
        r["pattern"] = classify(r)
    cands = [r for r in cands if r["pattern"]]
    stats["classified into a pattern"] = len(cands)
    cands.sort(key=rank)
    seen, chosen, per = set(), [], {s: 0 for s in QUOTA}
    for r in cands:
        fam = family_of(r["num"])
        if fam in seen:
            continue
        if per[r["pattern"]] >= QUOTA[r["pattern"]]:
            continue
        seen.add(fam)
        per[r["pattern"]] += 1
        r["why"] = "freq"
        chosen.append(r)
    # senior bar: top up with Hards
    hard_pool = [r for r in cands if r["diff"] == "Hard"]
    for slug in QUOTA:
        have = sum(1 for r in chosen if r["pattern"] == slug and r["diff"] == "Hard")
        pool = [r for r in hard_pool if r["pattern"] == slug and r not in chosen
                and (r["num"] in HARD_PREFER or r["freq"] >= 50)]
        pool.sort(key=lambda r: (HARD_PREFER.index(r["num"]) if r["num"] in HARD_PREFER else 99, -r["freq"], r["num"]))
        for r in pool:
            if have >= TARGET_HARD:
                break
            if family_of(r["num"]) in seen:
                continue
            seen.add(family_of(r["num"]))
            r["why"] = "Hard add-on"
            chosen.append(r)
            have += 1
    return chosen, stats


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    rows = list(parse(src))
    chosen, stats = pick(rows)
    for k, v in stats.items():
        print(f"- {k}: {v}")
    print(f"- picked: {len(chosen)}\n")
    for slug, title, quota in PATTERNS:
        group = [r for r in chosen if r["pattern"] == slug]
        print(f"### {slug.split('_')[0]} {title}  ({len(group)} picked; quota {quota} + Hard add-ons)\n")
        print("| LC | Problem | Diff | Freq | Why | Tags |\n|---:|---|---|---:|---|---|")
        for r in group:
            print(f"| {r['num']} | [{r['name']}]({r['url']}) | {r['diff']} | {r['freq']} | {r['why']} | {', '.join(r['tags'][:5])} |")
        print()
    print("order-by-frequency:", ", ".join(f"{r['num']}({r['freq']})" for r in sorted(chosen, key=rank)))


if __name__ == "__main__":
    main()
