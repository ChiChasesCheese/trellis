"""LeetCode data, before any analysis: where the problems live, the public frequency statistics, the classic lists and
the AnkiConnect client. Nothing here reads the learner's reviews; lc_analysis.py does that, and lc_tags.py only shapes the
deck from these fixed inputs.
"""
from __future__ import annotations

import csv
import json
import subprocess
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LC = ROOT / "vault/interviews/core/leetcode"
OUT = ROOT / "sources/local/lc"
DECKS = ["LeetCode Tops", "算法知识树（灵神题单）"]
PLAN_DECK = "1 今日计划"
PLAN_DECKS = (PLAN_DECK, "2 今日算法", "3 今日低层设计")  # the daily decks borrow cards from their home decks
GH = OUT / "github/leetcode-company-wise-problems"
GH_URL = "https://github.com/liquidslr/leetcode-company-wise-problems.git"
TARGETS = ("TikTok", "ByteDance")
OTHER = ROOT / "research/companies/tiktok/catalog/other_lists.json"  # classic lists by problem number (neetcode-gh, LeetCode study plans)
RECENT = ("1. Thirty Days", "2. Three Months", "3. Six Months")


def call(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    for _ in range(60):
        with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8765", body), timeout=600) as r:
            out = json.load(r)
        if out["error"] and "lifecycle" in out["error"]:
            time.sleep(3)
            continue
        if out["error"]:
            raise RuntimeError(f"{action}: {out['error']}")
        return out["result"]
    raise RuntimeError("Anki stayed busy")


def github_frequency() -> dict[str, dict]:
    """Per problem slug: target-company frequency (with whether it is recent) and cross-company breadth."""
    if not GH.exists():
        GH.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--depth", "1", GH_URL, str(GH)], check=True)

    def read(path: Path) -> dict[str, float]:
        if not path.exists():
            return {}
        return {r["Link"].rstrip("/").split("/problems/")[-1]: float(r["Frequency"] or 0) / 100
                for r in csv.DictReader(path.open(encoding="utf-8"))}

    out: dict[str, dict] = defaultdict(lambda: {"tiktok": 0.0, "tiktok_recent": False, "breadth": 0.0, "companies": 0})
    for d in sorted(x for x in GH.iterdir() if x.is_dir() and not x.name.startswith(".")):
        every = read(d / "5. All.csv")
        for slug, f in every.items():
            out[slug]["breadth"] += f
            out[slug]["companies"] += 1
        if d.name in TARGETS:
            recent: dict[str, float] = defaultdict(float)
            for w in RECENT:
                for slug, f in read(d / f"{w}.csv").items():
                    recent[slug] = max(recent[slug], f)
            for slug in set(every) | set(recent):
                t = 0.5 * every.get(slug, 0.0) + 0.5 * recent.get(slug, 0.0)
                o = out[slug]
                o["tiktok"] = max(o["tiktok"], t)
                o["tiktok_recent"] = o["tiktok_recent"] or slug in recent
    top = max(o["breadth"] for o in out.values()) or 1.0
    for o in out.values():
        o["breadth"] /= top
    return dict(out)


def recent_slugs(company: str) -> list[str]:
    """Problems a company asked in its last six months (any of the 30-day, 3-month, 6-month files)."""
    out = set()
    for w in RECENT:
        f = GH / company / f"{w}.csv"
        if f.exists():
            out |= {r["Link"].rstrip("/").split("/problems/")[-1] for r in csv.DictReader(f.open(encoding="utf-8"))}
    return sorted(out)


def classic_lists() -> dict[str, list[int]]:
    """Blind 75, NeetCode 150, LeetCode Hot 100, Top Interview 150: LeetCode problem numbers, in list order."""
    other = json.loads(OTHER.read_text(encoding="utf-8"))
    return {k: other[k] for k in ("Blind 75", "NeetCode 150", "LeetCode Hot 100", "Top Interview 150")}


def problem_numbers() -> dict[int, str]:
    """LeetCode number -> slug for every problem with a solution body."""
    out = {}
    for line in (OUT / "sections.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        head = r["title"].split()
        if len(head) > 1 and head[0] == "LC" and head[1].isdigit():
            out[int(head[1])] = r["slug"]
    return out
