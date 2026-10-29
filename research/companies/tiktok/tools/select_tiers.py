"""Choose tier A of the TikTok / ByteDance LeetCode deck: the ~200 problems that cover the most real interviews.

    uv run python research/companies/tiktok/tools/select_tiers.py      # re-tier index.json, write catalog/TIERS.md

Called by build_list.py too. Three signals, each turned into a share of its own total:

- reports (weight 0.5): the de-duplicated interview sightings of CATALOG.md §1 plus `catalog/refresh-*.json`, grouped
  into problem families; a sighting counts 0.5^(age / 180 days), so last month's report outweighs last year's.
- CodeTop (0.1): China-side ByteDance report counts (`catalog/codetop.json`), 0.5^(age of last report / 365 days).
- US lists (0.4): TikTok + ByteDance company-tag frequency (0-100) from lc_company.py, full weight in the 30-day and
  3-month windows, 0.8 in the 6-month window, 0.5 otherwise.

Tier A = the problems Chi pinned (`catalog/pinned.json`, on top of TARGET), every US sighting of the past year, every problem on the US TikTok / ByteDance company tags, anything seen anywhere in the last 30 days (the China-side long tail stays in B), then the top three problems of every pattern (so tier A
teaches every technique), then the TARGET highest scores (all of them, whatever else is already in). A family counts as covered when any of
its problems is in tier A; the report states how much of each signal tier A covers.
"""
from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CAT = ROOT / "research/companies/tiktok/catalog"
INDEX = ROOT / "research/companies/tiktok/index.json"
PATTERN_CARDS = ROOT / "vault/interviews/core/leetcode/tiktok/cards/patterns"
COMPANIES = ROOT / "vault/interviews/core/leetcode/companies"
TARGET = 200
PER_PATTERN = 3
MIX = {"reports": 0.5, "codetop": 0.1, "us": 0.4}

# CATALOG family (name prefix) -> the leaf that teaches it, when the family names no LeetCode number in the deck
FAMILY_VARIANT = {
    "LRU Cache (+TTL": "tt-lru-cache-ttl", "Rate limiter implementation": "tt-rate-limiter-implementation",
    "Number of Islands family": "tt-islands-follow-ups", "Largest number below N": "tt-largest-number-below-n-from-digits",
    "Reverse Nodes in k-Group": "tt-reverse-k-group-variants", "Deep merge": "tt-deep-merge-nested-json",
    "Basic Calculator I / II / III": "tt-basic-calculator-ladder",
    "Course Schedule / topological": "tt-course-schedule-output-path",
    "Currency conversion queries": "tt-currency-conversion-queries",
    "In-memory KV store with snapshot": "tt-kv-store-snapshot-restore", "Ring of 10 points": "tt-ring-walk-count",
    "Delete k consecutive elements": "tt-delete-window-balance-even-odd",
    "Contiguous / aligned memory allocator": "tt-contiguous-memory-allocator",
    "Path Sum III": "tt-path-sum-n-ary-prefix-sum", "Water and Jug": "tt-water-jug-shortest-operations",
    "Grid shortest path with obstacle removal": "tt-grid-min-cost-fuel-recharge",
    "Spiral Matrix with follow-up": "tt-spiral-matrix-constant-space",
    "Circular queue / O(1) deque": "tt-fixed-array-deque-o1", "Seller Task Scheduler": "tt-seller-task-scheduler",
    "Removable timestamp-ordered": "tt-removable-timestamp-task-scheduler",
    "Binary Tree Maximum Path Sum": "tt-max-path-sum-with-path", "Pythagorean triple": "tt-pythagorean-triple-in-array",
    "Valid Parenthesis String with": "tt-valid-parenthesis-string-print-all",
    "Nested comment tree": "tt-nested-comment-tree", "AI-assisted OrderValidator": "tt-ai-assisted-order-validator",
    "Flatten a multilevel list": "tt-flatten-multilevel-list-skip-empty",
    "Sorted array: values appearing": "tt-sorted-array-more-than-n-over-3",
    "Per-user per-day login": "tt-login-count-per-user-per-day",
    "Contiguous subarray with the largest min+max": "tt-subarray-max-min-plus-max",
    "Inorder iterator over a string": "tt-inorder-string-iterator", "get_chat_messages": "tt-chat-message-window-merge",
    "PercentileFinder": "tt-percentile-finder", "Weighted random sampler": "tt-weighted-sampler-dynamic-update",
    "IP range to the shortest CIDR": "tt-ip-range-to-cidr",
    "Implement a binary min-heap on an array": "tt-array-min-heap", "Hyper-operation": "tt-hyper-operation",
    "Tool-call log": "tt-tool-call-success-rate", "Maximize fish from decaying ponds": "tt-fish-decaying-ponds",
    "Concurrency-limited async task scheduler": "tt-concurrency-limited-runner",
    "Convert a number to its string form": "tt-number-to-string",
    "Count inverse pairs": "shu-zu-zhong-de-ni-xu-dui-lcof", "First 10,000 / n-th prime": "count-primes",
    "BFS maze / map shortest path": "shortest-path-in-binary-matrix",
    "Enumerate all simple directed paths": "tt-all-simple-paths",
    "Idempotent versioned database update": "tt-idempotent-versioned-update",
    "Most frequent element, ties": "tt-most-frequent-ties-smaller", "Longest zigzag path in a grid": "tt-longest-zigzag-grid-path",
    "Probability one fair die beats another": "tt-die-beats-probability",
    "streaming event tracer for an agent": "tt-agent-tool-call-tracer",
}


def day(s: str) -> date:
    """'2026-10-05' or a month-only '2026-10' (read as the 15th)."""
    s = (s or "").strip()
    return date.fromisoformat(s if len(s) == 10 else f"{s}-15") if re.match(r"\d{4}-\d\d", s) else date(2000, 1, 1)


def families() -> list[dict]:
    """CATALOG.md §1 rows, plus the sightings of every refresh file merged into them (or into new families)."""
    rows = []
    for line in (CAT / "CATALOG.md").read_text(encoding="utf-8").split("\n## 2.")[0].splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 13 or not c[0].isdigit():
            continue
        name = re.sub(r"\s*\[(custom|OA)\]", "", c[2].replace("**", "")).strip()
        us = sum(int(x) for x in re.findall(r"(?:US|SG|OTHER) (\d+)", c[8]))
        rows.append({"family": name, "lc": [int(x) for x in re.findall(r"\d+", c[4])], "refs": int(c[7]),
                     "dates": [c[9]] * int(c[7]), "regions": ["US"] * us + ["CN"] * (int(c[7]) - us),
                     "oa": "[OA]" in c[2]})
    by_name = {r["family"]: r for r in rows}
    for f in sorted(CAT.glob("refresh-*.json")):
        for s in json.loads(f.read_text(encoding="utf-8")).get("sightings", []):
            if s.get("scope", "").startswith("out"):
                continue
            lc = [int(x) for x in s.get("lc") or []]
            fam = by_name.get(s.get("family") or "") or next((r for r in rows if lc and lc[0] in r["lc"]), None)
            if fam is None:
                fam = {"family": s.get("custom") or f"LC {lc[0]}", "lc": lc, "refs": 0, "dates": [], "regions": [],
                       "oa": s.get("round") == "OA"}
                rows.append(fam)
                by_name[fam["family"]] = fam
            fam["refs"] += 1
            fam["dates"].append(s.get("date", ""))
            fam["regions"].append("CN" if s.get("region") == "CN" else "US")
    return rows


def us_rows() -> dict[str, dict]:
    row = re.compile(r"^\| (\d+) \| \[.+\]\(https://leetcode\.com/problems/([^/]+)/\) \| \w+ \| (\d+) \|")
    out: dict[str, dict] = {}
    for co in ("tiktok", "bytedance"):
        for line in (COMPANIES / f"{co}.md").read_text(encoding="utf-8").splitlines():
            if m := row.match(line):
                prev = out.get(m.group(2), {"freq": 0})
                out[m.group(2)] = {"id": int(m.group(1)), "freq": max(prev["freq"], int(m.group(3)))}
    return out


def pattern_map() -> dict[int, set[str]]:
    """LC number -> patterns whose problem-list card names it."""
    out: dict[int, set[str]] = {}
    for f in PATTERN_CARDS.glob("tlc-patterns-*-problems.md"):
        pat = re.match(r"tlc-patterns-(.+?)-\d+-problems", f.stem)
        if not pat:
            continue
        for n in re.findall(r"LC\s*(\d+)", f.read_text(encoding="utf-8").split("## A", 1)[-1]):
            out.setdefault(int(n), set()).add(pat.group(1))
    return out


def assign(index: dict[str, dict], today: date | None = None) -> dict:
    """Set p["tier"], p["score"] and p["a_reason"] on every problem of `index`; return the coverage report."""
    today = today or date.today()
    cut30 = today - timedelta(days=30)
    cut1y = today - timedelta(days=365)  # Chi (2026-10-29): every US sighting of the past year goes to tier A
    by_id: dict[int, list[str]] = {}
    for slug, p in index.items():
        if p.get("id"):
            by_id.setdefault(p["id"], []).append(slug)

    # reports: each family's recency-weighted mass goes to its members (primary 1.0, variant 1.0 / 0.5, others 0.3)
    fams = families()
    rep: dict[str, float] = {}
    members: list[tuple[dict, list[str], float]] = []
    for fam in fams:
        mass = sum(0.5 ** ((today - day(d)).days / 180) for d in fam["dates"])
        slugs: list[tuple[str, float]] = []
        for i, n in enumerate(fam["lc"]):
            slugs += [(s, 1.0 if i == 0 else 0.3) for s in by_id.get(n, [])]
        v = next((v for k, v in FAMILY_VARIANT.items() if fam["family"].startswith(k)), None)
        if v and v in index:
            slugs.append((v, 1.0 if not slugs or fam["refs"] >= 3 else 0.5))
        for s, w in slugs:
            rep[s] = rep.get(s, 0) + w * mass
        members.append((fam, [s for s, _ in slugs], mass))
        fam["recent"] = any(day(d) >= cut30 for d in fam["dates"])
        fam["us_year"] = any(day(d) >= cut1y and r == "US" for d, r in zip(fam["dates"], fam["regions"]))

    snap = json.loads((CAT / "codetop.json").read_text(encoding="utf-8"))["rows"]
    ct_all = {r["slug"]: r["reports"] * 0.5 ** ((today - day(r["last_seen"])).days / 365) for r in snap}
    ct_recent = {r["slug"] for r in snap if day(r["last_seen"]) >= cut30}
    win = {"30d": 1.0, "3m": 1.0, "6m": 0.8}
    us_all = {s: r["freq"] * win.get(index.get(s, {}).get("window", ""), 0.5) for s, r in us_rows().items()}
    us_recent = {s for s, p in index.items() if p.get("window") == "30d"}

    tot = {"reports": sum(m for _, _, m in members) or 1, "codetop": sum(ct_all.values()) or 1,
           "us": sum(us_all.values()) or 1}
    for slug, p in index.items():
        p["score"] = round(100 * (MIX["reports"] * rep.get(slug, 0) / tot["reports"]
                                  + MIX["codetop"] * ct_all.get(slug, 0) / tot["codetop"]
                                  + MIX["us"] * us_all.get(slug, 0) / tot["us"]), 4)

    a: dict[str, str] = {}
    pinned = CAT / "pinned.json"  # 0. problems Chi asked to keep in tier A
    for s in json.loads(pinned.read_text(encoding="utf-8"))["A"] if pinned.exists() else []:
        if s in index:
            a[s] = "pinned"
    for fam, slugs, _ in members:  # 1. seen anywhere in the last 30 days, or in the US in the past year
        reason = "us1y" if fam["us_year"] else "30d" if fam["recent"] else ""
        if reason and slugs:
            a.setdefault(max(slugs, key=lambda s: index[s]["score"]), reason)
            for s in slugs:  # the TikTok version is what was actually asked
                if s.startswith("tt-"):
                    a.setdefault(s, reason)
    for f in sorted(CAT.glob("refresh-*.json")):  # every problem a recent report names, follow-ups included
        for row in json.loads(f.read_text(encoding="utf-8")).get("sightings", []):
            recent = day(row.get("date", "")) >= (cut1y if row.get("region") != "CN" else cut30)
            if not row.get("scope", "").startswith("out") and recent:
                for n in row.get("lc") or []:
                    for s in by_id.get(int(n), []):
                        a.setdefault(s, "us1y" if row.get("region") != "CN" else "30d")
    for s, p in index.items():  # US company tags (any window) and anything CodeTop saw in the last 30 days
        if "tiktok" in p["companies"] or "bytedance" in p["companies"]:
            a.setdefault(s, "ustag")
        elif s in ct_recent:
            a.setdefault(s, "30d")
    pats = pattern_map()  # 2. every pattern gets its best problems
    for pat in sorted({x for v in pats.values() for x in v}):
        cands = sorted((s for s, p in index.items() if pat in pats.get(p.get("id") or -1, set())),
                       key=lambda s: -index[s]["score"])
        have = sum(1 for s in a if pat in pats.get(index[s].get("id") or -1, set()))
        for s in cands:
            if have >= PER_PATTERN:
                break
            if s not in a:
                a[s] = f"pattern:{pat}"
                have += 1
    for s in sorted(index, key=lambda s: -index[s]["score"])[:TARGET]:  # 3. the TARGET highest scores, always
        a.setdefault(s, "score")
    for s, p in index.items():
        p["tier"] = "A" if s in a else "B"
        p["a_reason"] = a.get(s, "")

    def share(weights: dict[str, float], total: float) -> float:
        return round(100 * sum(w for s, w in weights.items() if s in a) / total, 1)
    covered = [(f, m) for f, slugs, m in members if any(s in a for s in slugs)]
    return {
        "a": len(a), "b": len(index) - len(a), "reasons": {k: sum(1 for v in a.values() if v.startswith(k))
                                                           for k in ("pinned", "us1y", "30d", "ustag", "pattern", "score")},
        "reports_weighted": round(100 * sum(m for _, m in covered) / tot["reports"], 1),
        "reports_raw": round(100 * sum(f["refs"] for f, _ in covered) / sum(f["refs"] for f in fams), 1),
        "reports_reachable": round(100 * sum(f["refs"] for f, s, _ in members if s) / sum(f["refs"] for f in fams), 1),
        "codetop": share(ct_all, tot["codetop"]), "us": share(us_all, tot["us"]),
        "uncovered": sorted(((f["refs"], f["family"], f["lc"]) for f, s, _ in members if not s), reverse=True),
        "families": len(fams), "sightings": sum(f["refs"] for f in fams),
    }


def main() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    r = assign(index)
    INDEX.write_text(json.dumps(dict(sorted(index.items(), key=lambda kv: (kv[1]["tier"], -kv[1]["score"]))),
                                ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in r.items() if k != "uncovered"}, ensure_ascii=False))
    print("uncovered families (refs, name, LC):", *r["uncovered"][:25], sep="\n  ")


if __name__ == "__main__":
    main()
