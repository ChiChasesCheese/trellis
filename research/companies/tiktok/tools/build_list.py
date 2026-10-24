"""TikTok + ByteDance LeetCode list for the `tiktok-lc` deck.

    uv run python research/companies/tiktok/tools/build_list.py            # index.json + statements
    uv run python research/companies/tiktok/tools/build_list.py --no-fetch # index.json from the tables only

Reads vault/interviews/core/leetcode/companies/{tiktok,bytedance}.md (made by lc_company.py), unions them, keeps
tier A (seen in the last 6 months, or frequency >= 70) and tier B (frequency >= 50) of either company, drops SQL
problems, and orders by the higher of the two frequencies. Facts go to research/companies/tiktok/index.json
(committed); problem statements from leetcode.cn go to sources/local/tiktok-lc/<slug>.txt (gitignored: the repo is
public and the statements are LeetCode's text).
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
COMPANIES = ROOT / "vault/interviews/core/leetcode/companies"
OUT = ROOT / "research/companies/tiktok/index.json"
STATEMENTS = ROOT / "sources/local/tiktok-lc"
ROW = re.compile(r"^\| (\d+) \| \[(.+)\]\(https://leetcode\.com/problems/([^/]+)/\) \| (\w+) \| (\d+) \| (✓?) \| (✓?) \| (.*?) \|")
QUERY = ("query q($s:String!){question(titleSlug:$s){questionFrontendId translatedTitle title difficulty "
         "translatedContent content}}")


def table(company: str) -> dict[str, dict]:
    out = {}
    for line in (COMPANIES / f"{company}.md").read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            n, title, slug, diff, freq, recent, both, tags = m.groups()
            out[slug] = {"id": int(n), "title": title, "slug": slug, "difficulty": diff, "freq": int(freq),
                         "recent": bool(recent), "tags": [t.strip() for t in tags.split(",") if t.strip()]}
    return out


def tier(p: dict) -> str:
    return "A" if p["recent"] or p["freq"] >= 70 else ("B" if p["freq"] >= 50 else "C")


def to_text(raw: str) -> str:
    text = re.sub(r"<sup>\s*(.*?)\s*</sup>", r"^\1", raw or "")  # 10<sup>5</sup> -> 10^5, not 105
    text = re.sub(r"<(pre|p|div|li|ul|ol|br)[^>]*>", "\n", text)
    text = re.sub(r"</?[a-zA-Z][^>]*>", "", text)  # never strip a bare `<` from constraints
    text = html.unescape(text).replace("\xa0", " ")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def fetch(slug: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"s": slug}}).encode()
    req = urllib.request.Request("https://leetcode.cn/graphql/", data=body,
                                 headers={"Content-Type": "application/json", "Referer": "https://leetcode.cn"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["data"]["question"] or {}


def doocs(pid: int) -> str:
    """Chinese statement of a premium problem from doocs/leetcode (leetcode.cn hides those)."""
    import base64
    import subprocess
    lo = pid // 100 * 100
    rng = f"{lo:04d}-{lo + 99:04d}"
    names = subprocess.run(["gh", "api", f"repos/doocs/leetcode/contents/solution/{rng}", "--jq", ".[].name"],
                           capture_output=True, text=True).stdout.splitlines()
    name = next((n for n in names if n.startswith(f"{pid:04d}.")), None)
    if not name:
        return ""
    raw = subprocess.run(["gh", "api", f"repos/doocs/leetcode/contents/solution/{rng}/{name}/README.md"],
                         capture_output=True, text=True).stdout
    md = base64.b64decode(json.loads(raw)["content"]).decode()
    m = re.search(r"<!-- description:start -->(.*?)<!-- description:end -->", md, re.S)
    return to_text(m.group(1) if m else "")


def main(argv: list[str]) -> int:
    t, b = table("tiktok"), table("bytedance")
    merged: dict[str, dict] = {}
    for company, rows in (("tiktok", t), ("bytedance", b)):
        for slug, p in rows.items():
            q = merged.setdefault(slug, {**p, "companies": {}})
            q["companies"][company] = {"freq": p["freq"], "recent": p["recent"], "tier": tier(p)}
            q["freq"] = max(q["freq"], p["freq"])
            q["recent"] = q["recent"] or p["recent"]
    keep = [p for p in merged.values()
            if min(c["tier"] for c in p["companies"].values()) in "AB" and "Database" not in p["tags"]]
    for p in keep:
        p["tier"] = min(c["tier"] for c in p["companies"].values())
    keep.sort(key=lambda p: (p["tier"], -p["freq"], p["id"]))
    if "--no-fetch" not in argv:
        STATEMENTS.mkdir(parents=True, exist_ok=True)
        for i, p in enumerate(keep, 1):
            dest = STATEMENTS / f"{p['slug']}.txt"
            if not dest.exists():
                q = fetch(p["slug"])
                text = to_text(q.get("translatedContent") or q.get("content") or "") or doocs(p["id"])
                dest.write_text(text, encoding="utf-8")
                time.sleep(0.4)
                p["title_zh"] = q.get("translatedTitle") or ""
            else:
                p["title_zh"] = (json.loads(OUT.read_text()) if OUT.exists() else {}).get(p["slug"], {}).get("title_zh", "")
            p["statement_chars"] = len((STATEMENTS / f"{p['slug']}.txt").read_text(encoding="utf-8"))
            print(f"{i:3d} {p['tier']} {p['freq']:3d} {p['slug']} ({p['statement_chars']} chars)", flush=True)
    OUT.write_text(json.dumps({p["slug"]: p for p in keep}, ensure_ascii=False, indent=1), encoding="utf-8")
    tiers = {k: sum(p["tier"] == k for p in keep) for k in "AB"}
    print(f"{len(keep)} problems (A {tiers['A']} / B {tiers['B']}) -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
