"""TikTok + ByteDance LeetCode list for the `tiktok-lc` deck.

    uv run python research/companies/tiktok/tools/build_list.py            # index.json + statements
    uv run python research/companies/tiktok/tools/build_list.py --no-fetch # index.json from the tables only

Reads vault/interviews/core/leetcode/companies/{tiktok,bytedance}.md (made by lc_company.py), unions them, keeps
tier A (seen in the last 6 months, or frequency >= 70) and tier B (frequency >= 50) of either company, drops SQL
problems, and orders by the higher of the two frequencies. China-side ByteDance interviews draw on a different pool, so
the CodeTop list for 字节跳动 (reports from Chinese forums, with a count and a last-seen date) is unioned in, one list for
learning: CN tier A = >= 50 reports or seen in the last 30 days, B = >= 20 reports or seen in the last 3 months; a
problem takes the better of its US and CN tiers. Order inside a tier: the higher of the US frequency (0-100) and the CN
report count as a percentile of the CodeTop list (0-100). Facts go to research/companies/tiktok/index.json
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
         "translatedContent content categoryTitle topicTags{name}}}")
# Recent windows, newest first: (label, primary-repo file, secondary-repo file)
WINDOWS = [("30d", "1. Thirty Days", "thirty-days"), ("3m", "2. Three Months", "three-months"),
           ("6m", "3. Six Months", "six-months")]
DIRS = {"tiktok": ("TikTok", "tiktok"), "bytedance": ("ByteDance", "bytedance")}


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


def gh_csv(repo: str, path: str) -> list[dict]:
    import base64
    import csv
    import io
    import subprocess
    out = subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}"], capture_output=True, text=True)
    if out.returncode:
        return []
    return list(csv.DictReader(io.StringIO(base64.b64decode(json.loads(out.stdout)["content"]).decode())))


def windows() -> dict[str, dict]:
    """slug -> {"window": newest window it appears in, "freq": best frequency seen there}. The company tables only
    list problems from each repo's all-time file, so a problem seen only recently is missing there."""
    seen: dict[str, dict] = {}
    for label, pfile, sfile in reversed(WINDOWS):  # oldest first, so newer windows overwrite
        for pdir, sdir in DIRS.values():
            rows = [(r.get("Link", ""), r.get("Frequency", "0")) for r in
                    gh_csv("liquidslr/leetcode-company-wise-problems", f"{pdir}/{pfile}.csv")]
            rows += [(r.get("URL", ""), r.get("Frequency %", "0").rstrip("%")) for r in
                     gh_csv("snehasishroy/leetcode-companywise-interview-questions", f"{sdir}/{sfile}.csv")]
            for url, freq in rows:
                m = re.search(r"/problems/([^/]+)", url or "")
                if m:
                    slug = m.group(1)
                    prev = seen.get(slug, {})
                    seen[slug] = {"window": label, "freq": max(float(freq or 0), prev.get("freq", 0.0))}
    return seen


CODETOP = "https://codetop.cc/api/questions/?page={page}&search=&ordering=-frequency&company=1"  # 1 = 字节跳动


def codetop(today: str) -> dict[str, dict]:
    """slug -> CodeTop facts for the problems that pass the CN rule. Non-LeetCode extras (补充题) get a
    `codetop-supp-<n>` slug and carry CodeTop's own statement."""
    from datetime import date, timedelta
    t = date.fromisoformat(today)
    d30, d90 = str(t - timedelta(days=30)), str(t - timedelta(days=90))
    rows, page = [], 1
    while True:
        with urllib.request.urlopen(CODETOP.format(page=page), timeout=30) as r:
            data = json.loads(r.read())
        rows += data["list"]
        if not data["list"] or len(rows) >= data["count"]:
            break
        page += 1
        time.sleep(0.3)
    out = {}
    for x in rows:
        seen = x["time"][:10]
        cn_tier = "A" if x["value"] >= 50 or seen >= d30 else ("B" if x["value"] >= 20 or seen >= d90 else "")
        if not cn_tier:
            continue
        lc = x["leetcode"]
        fid = str(lc["frontend_question_id"])
        if fid.startswith("补充题"):
            slug, kind = f"codetop-supp-{fid.removeprefix('补充题').strip()}", "supplement"
        else:
            slug, kind = lc["slug_title"], ("leetcode" if fid.isdigit() else "lcof")
        out[slug] = {"fid": fid, "title_zh": lc["title"], "difficulty": {1: "Easy", 2: "Medium", 3: "Hard"}.get(
            lc.get("level"), ""), "reports": x["value"], "last_seen": seen, "cn_tier": cn_tier, "kind": kind,
            "content": lc.get("content") or ""}
    return out


def main(argv: list[str]) -> int:
    t, b = table("tiktok"), table("bytedance")
    merged: dict[str, dict] = {}
    for company, rows in (("tiktok", t), ("bytedance", b)):
        for slug, p in rows.items():
            q = merged.setdefault(slug, {**p, "companies": {}})
            q["companies"][company] = {"freq": p["freq"], "recent": p["recent"], "tier": tier(p)}
            q["freq"] = max(q["freq"], p["freq"])
            q["recent"] = q["recent"] or p["recent"]
    recent = windows()
    for slug, w in recent.items():
        if slug not in merged:  # seen recently but absent from the all-time tables
            q = fetch(slug)
            if not q or q.get("categoryTitle") == "Database":
                continue
            merged[slug] = {"id": int(q["questionFrontendId"]), "title": q["title"], "slug": slug,
                            "difficulty": q["difficulty"], "freq": int(w["freq"]), "recent": True,
                            "tags": [t["name"] for t in q.get("topicTags") or []],
                            "companies": {"tiktok": {"freq": int(w["freq"]), "recent": True, "tier": "A"}}}
    for slug, p in merged.items():
        p["window"] = recent.get(slug, {}).get("window", "")
    keep = [p for p in merged.values()
            if (p["window"] or min(c["tier"] for c in p["companies"].values()) in "AB")
            and "Database" not in p["tags"]]
    for p in keep:
        p["tier"] = "A" if p["window"] else min(c["tier"] for c in p["companies"].values())
    from datetime import date
    cn = codetop(str(date.today()))
    have = {p["slug"] for p in keep}
    for p in keep:
        if p["slug"] in cn:
            c = cn[p["slug"]]
            p["companies"]["bytedance_cn"] = {"reports": c["reports"], "last_seen": c["last_seen"], "tier": c["cn_tier"]}
    ranked = sorted(c["reports"] for c in cn.values())
    def pct(n: int) -> int:
        return round(100 * sum(r <= n for r in ranked) / len(ranked))
    for p in keep:
        c = p["companies"].get("bytedance_cn")
        if c:
            p["tier"] = min(p["tier"], c["tier"])
            p["freq"] = max(p["freq"], pct(c["reports"]))
    for slug, c in cn.items():
        if slug in have:
            continue
        keep.append({"id": int(c["fid"]) if c["fid"].isdigit() else 0, "fid": c["fid"], "title": c["title_zh"],
                     "title_zh": c["title_zh"], "slug": slug, "difficulty": c["difficulty"], "freq": pct(c["reports"]),
                     "recent": False, "window": "", "tags": [], "tier": c["cn_tier"], "kind": c["kind"],
                     "companies": {"bytedance_cn": {"reports": c["reports"], "last_seen": c["last_seen"],
                                                    "tier": c["cn_tier"]}}})
        if c["kind"] == "supplement" and "--no-fetch" not in argv:
            STATEMENTS.mkdir(parents=True, exist_ok=True)
            (STATEMENTS / f"{slug}.txt").write_text(to_text(c["content"]), encoding="utf-8")
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
                p["title_zh"] = q.get("translatedTitle") or p.get("title_zh", "")
            else:
                p["title_zh"] = p.get("title_zh") or (json.loads(OUT.read_text()) if OUT.exists() else {}).get(
                    p["slug"], {}).get("title_zh", "")
            p["statement_chars"] = len((STATEMENTS / f"{p['slug']}.txt").read_text(encoding="utf-8"))
            print(f"{i:3d} {p['tier']} {p['freq']:3d} {p['slug']} ({p['statement_chars']} chars)", flush=True)
    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for p in keep:  # facts gathered by an earlier fetch survive a --no-fetch run
        for key in ("title_zh", "statement_chars", "statement_source"):
            if not p.get(key) and previous.get(p["slug"], {}).get(key):
                p[key] = previous[p["slug"]][key]
    OUT.write_text(json.dumps({p["slug"]: p for p in keep}, ensure_ascii=False, indent=1), encoding="utf-8")
    tiers = {k: sum(p["tier"] == k for p in keep) for k in "AB"}
    print(f"{len(keep)} problems (A {tiers['A']} / B {tiers['B']}) -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
