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
Extra : python3 -I coding/pick.py --extra [path]  -> the optional second track (patterns 12-16: backtracking, greedy,
        trie, union-find, matrix simulation). Same A-tier + recent + both filter; skips every problem the 11-pattern
        run already picked; quota applies to non-Hard problems, Hards are filled separately (EX_HARD_PREFER, then freq).
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


# ---------------------------------------------------------------- optional track: patterns 12-16
EXTRA_PATTERNS = [
    ("12_backtracking", "Backtracking (choose / explore / un-choose)", 4),
    ("13_greedy", "Greedy (exchange argument)", 4),
    ("14_trie", "Trie (prefix tree)", 4),
    ("15_union_find", "Union-Find (disjoint set union)", 4),
    ("16_matrix_simulation", "Matrix simulation / in-place grid work", 5),
]
EX_QUOTA = {s: q for s, _, q in EXTRA_PATTERNS}
BT, GD, TRIE, UF, MX = (p[0] for p in EXTRA_PATTERNS)
EX_TAG_RULES = [("Union-Find", UF), ("Trie", TRIE), ("Backtracking", BT), ("Greedy", GD)]
EX_OVERRIDE = {
    212: TRIE,   # Word Search II: backtracking on a grid, but the trie is the point
    472: TRIE, 140: None,   # 140 Word Break II: backtracking + memo, not taught (mentioned in 14)
    126: None,               # Word Ladder II: BFS + path rebuild, not taught
    692: None,               # Top K Frequent Words: heap lecture (05) territory
    494: None, 698: None, 301: None, 980: None,
    68: MX,                  # Text Justification: pure simulation Hard (no Matrix tag)
    36: MX, 48: MX, 73: MX,  # tag "Matrix" alone is too broad, so these three are named explicitly
    11: None, 435: None, 410: None, 253: None, 767: None,   # already taught in 02/03/05/07
}
EX_PREFER = [55, 621, 22, 79]
EX_HARD_PREFER = [51, 37, 135, 871, 212, 472, 305, 827, 68]
EX_TARGET_HARD = 2
EX_FAMILIES = dict(FAMILIES, spiral={54, 59}, **{"word-break": {139, 140}})


def classify_extra(r):
    if r["num"] in EX_OVERRIDE:
        return EX_OVERRIDE[r["num"]]
    if "Matrix" in r["tags"] and "Simulation" in r["tags"]:
        return MX
    for tag, slug in EX_TAG_RULES:
        if tag in r["tags"]:
            return slug
    return None


def extra_family(num):
    for fam, members in EX_FAMILIES.items():
        if num in members:
            return fam
    return f"solo-{num}"


def pick_extra(rows, base_chosen):
    taken = {r["num"] for r in base_chosen}
    seen = {family_of(n) for n in taken} | {extra_family(n) for n in taken}
    cands = [r for r in rows
             if r["tier"] == "A" and r["recent"] and r["both"] and r["num"] not in taken
             and not (set(r["tags"]) & EXCLUDE_TAGS) and r["num"] not in EXCLUDE_NUMS]
    for r in cands:
        r["pattern"] = classify_extra(r)
    cands = [r for r in cands if r["pattern"]]

    def key(r):
        pref = EX_PREFER.index(r["num"]) if r["num"] in EX_PREFER else len(EX_PREFER)
        return (-r["freq"], pref, r["num"])

    cands.sort(key=key)
    chosen, per = [], {s: 0 for s in EX_QUOTA}
    for r in cands:
        if r["diff"] == "Hard" or extra_family(r["num"]) in seen or per[r["pattern"]] >= EX_QUOTA[r["pattern"]]:
            continue
        seen.add(extra_family(r["num"]))
        per[r["pattern"]] += 1
        r["why"] = "freq"
        chosen.append(r)
    for slug in EX_QUOTA:
        pool = [r for r in cands if r["pattern"] == slug and r["diff"] == "Hard"
                and (r["num"] in EX_HARD_PREFER or r["freq"] >= 50)]
        pool.sort(key=lambda r: (EX_HARD_PREFER.index(r["num"]) if r["num"] in EX_HARD_PREFER else 99, -r["freq"], r["num"]))
        have = 0
        for r in pool:
            if have >= EX_TARGET_HARD:
                break
            if extra_family(r["num"]) in seen:
                continue
            seen.add(extra_family(r["num"]))
            r["why"] = "Hard add-on"
            chosen.append(r)
            have += 1
    return chosen, {"candidates after filter + classification": len(cands)}


def main_extra(rows):
    base, _ = pick(rows)
    chosen, stats = pick_extra(rows, base)
    for k, v in stats.items():
        print(f"- {k}: {v}")
    print(f"- picked: {len(chosen)}\n")
    for slug, title, quota in EXTRA_PATTERNS:
        group = sorted([r for r in chosen if r["pattern"] == slug], key=lambda r: (r["diff"] == "Hard", -r["freq"], r["num"]))
        print(f"### {slug.split('_')[0]} {title}  ({len(group)} picked; quota {quota} + Hard add-ons)\n")
        print("| LC | Problem | Diff | Freq | Why | Tags |\n|---:|---|---|---:|---|---|")
        for r in group:
            print(f"| {r['num']} | [{r['name']}]({r['url']}) | {r['diff']} | {r['freq']} | {r['why']} | {', '.join(r['tags'][:5])} |")
        print()
    print("order-by-frequency:", ", ".join(f"{r['num']}({r['freq']})" for r in sorted(chosen, key=key_by_freq)))


def key_by_freq(r):
    return (-r["freq"], r["num"])


def main():
    args = [a for a in sys.argv[1:] if a != "--extra"]
    src = Path(args[0]) if args else DEFAULT_SRC
    rows = list(parse(src))
    if "--extra" in sys.argv[1:]:
        return main_extra(rows)
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
