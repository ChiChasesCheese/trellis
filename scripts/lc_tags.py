"""Tags on the one card each LeetCode problem has, so a list or a company is a view, not a deck (Chi, 2026-11-14).

    uv run python scripts/lc_tags.py            # dry run: how many problems each tag would get
    uv run python scripts/lc_tags.py --apply    # rewrite the 榜单:: and 公司:: tags in Anki (desktop Anki running)

Every problem's single card is its card in the 0x3F knowledge tree (`lct-<slug>`, domain leetcode-tree). It carries:
- `榜单::Blind_75`, `榜单::NeetCode_150`, `榜单::Hot_100`, `榜单::Top_Interview_150`: the classic lists;
- `榜单::LeetCode_Tops`: the union of those lists and the company-frequency 80/20 selection (research/leetcode-tops);
- `榜单::TikTok_近半年`: asked by TikTok / ByteDance in the last six months;
- `已做过`: Chi solved it on LeetCode (the ledger skeleton/leetcode-daily.yaml, filled by scripts/leetcode_daily.py);
- `公司::<Company>`: the company asked it, from the public company-wise lists (sources/local/lc/github; companies in
  COMPANIES that have a folder there) and from our own company research (sources/local/lc/company_extra.json,
  {"Cerebras": [slug, …]}).
Study a view by searching the tag (Anki browser, or a filtered deck on the phone: `tag:公司::Amazon`), or deal it into a
sprint deck (scripts/lc_view.py). Other copies of a problem (old decks) lose these tags. Fields, decks and scheduling are
untouched; anki_refresh.py rewrites fields only, so the tags survive.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from lc_data import GH, call, classic_lists, recent_slugs

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "vault/interviews/core/leetcode/problems"
EXTRA = ROOT / "sources/local/lc/company_extra.json"
LISTS = {"Blind 75": "Blind_75", "NeetCode 150": "NeetCode_150", "LeetCode Hot 100": "Hot_100", "Top Interview 150": "Top_Interview_150"}
COMPANIES = ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Netflix", "Uber", "Airbnb", "Stripe", "Snowflake", "Databricks",
             "TikTok", "ByteDance", "NVIDIA", "OpenAI", "Anthropic", "Roblox", "LinkedIn", "Pinterest", "Salesforce", "Oracle",
             "Bloomberg", "Citadel", "Jane Street", "Two Sigma", "Hudson River Trading", "Millennium", "Coinbase", "Robinhood",
             "DoorDash", "Instacart", "Lyft", "Adobe", "Intuit", "PayPal", "Visa", "Capital One", "Goldman Sachs", "Atlassian",
             "Abnormal Security", "Headlands Technologies", "Cerebras"]
PREFIXES = ("榜单::", "公司::", "已做过")
SOLVED = ROOT / "skeleton/leetcode-daily.yaml"


def numbers() -> dict[int, str]:
    """LeetCode number -> slug, read off every answer body's title (**LC <n> …**)."""
    out = {}
    for f in PROBLEMS.glob("*.md"):
        m = re.search(r"^\*\*LC (\d+) ", f.read_text(encoding="utf-8", errors="ignore"), re.M)
        if m:
            out[int(m.group(1))] = f.stem
    return out


def company_slugs(name: str) -> set[str]:
    f = GH / name / "5. All.csv"
    if not f.exists():
        return set()
    return {r["Link"].rstrip("/").split("/problems/")[-1] for r in csv.DictReader(f.open(encoding="utf-8"))}


def wanted() -> dict[str, set[str]]:
    """slug -> tags."""
    have = {f.stem for f in PROBLEMS.glob("*.md")}
    by_num = numbers()
    tags: dict[str, set[str]] = defaultdict(set)
    for name, nums in classic_lists().items():
        for n in nums:
            if by_num.get(n):
                tags[by_num[n]] |= {f"榜单::{LISTS[name]}", "榜单::LeetCode_Tops"}
    sel = ROOT / "research/leetcode-tops/selection.json"
    for p in json.loads(sel.read_text(encoding="utf-8")) if sel.exists() else []:
        if p["slug"] in have:
            tags[p["slug"]].add("榜单::LeetCode_Tops")
    for s in set(recent_slugs("TikTok")) | set(recent_slugs("ByteDance")):
        if s in have:
            tags[s].add("榜单::TikTok_近半年")
    for c in COMPANIES:
        for s in company_slugs(c) & have:
            tags[s].add("公司::" + c.replace(" ", "_"))
    if SOLVED.exists():  # leaf ids end in the problem's slug
        for s in set(re.findall(r"^\s*- id: \S+\.([a-z0-9-]+)$", SOLVED.read_text(encoding="utf-8"), re.M)) & have:
            tags[s].add("已做过")
    for c, slugs in (json.loads(EXTRA.read_text(encoding="utf-8")) if EXTRA.exists() else {}).items():
        for s in set(slugs) & have:
            tags[s].add("公司::" + c.replace(" ", "_"))
    return tags


def main() -> int:
    apply = "--apply" in sys.argv
    tags = wanted()
    count: dict[str, int] = defaultdict(int)
    for ts in tags.values():
        for t in ts:
            count[t] += 1
    for t in sorted(count, key=lambda t: (not t.startswith("榜单"), -count[t])):
        print(f"{count[t]:5}  {t}")
    if not apply:
        return 0
    nids = call("findNotes", query='"tag:id::lct-*" -"tag:id::lct-learn-*" -"deck:LeetCode Tops::99*"')  # not the old archive
    notes = []
    for i in range(0, len(nids), 500):
        notes += call("notesInfo", notes=nids[i:i + 500])
    canonical = {}
    for n in notes:
        ident = next((t[4:] for t in n["tags"] if t.startswith("id::lct-")), None)
        if ident:
            canonical[ident[4:]] = n
    stale = call("findNotes", query=" OR ".join(f'"tag:{p}*"' for p in PREFIXES))
    for i in range(0, len(stale), 500):  # every old list / company tag goes, on any copy
        for n in call("notesInfo", notes=stale[i:i + 500]):
            old = [t for t in n["tags"] if t.startswith(PREFIXES)]
            if old:
                call("removeTags", notes=[n["noteId"]], tags=" ".join(old))
    by_tags: dict[str, list[int]] = defaultdict(list)
    for slug, ts in tags.items():
        n = canonical.get(slug)
        if n:
            by_tags[" ".join(sorted(ts))].append(n["noteId"])
    for ts, ids in by_tags.items():
        call("addTags", notes=ids, tags=ts)
    missing = sorted(s for s in tags if s not in canonical)
    print(f"tagged {sum(len(v) for v in by_tags.values())} problems; {len(missing)} have no tree card yet: {' '.join(missing[:10])}")
    call("sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
