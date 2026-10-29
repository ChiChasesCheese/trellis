"""Write each problem's frequency facts into the header line of its cards, like the Amazon deck does.

    uv run python research/companies/tiktok/tools/stamp_headers.py [--dry-run]

The header line of a whole-answer card and of a `-1-signal` card is `**LC n 名字**｜<难度> · …`. Everything after the
difficulty is rewritten from the data: TikTok / ByteDance company-tag frequency (0-100, with the US recent window), the
number of interview sightings in the past year, the China-side CodeTop count, and the most recent date seen anywhere.
Re-run after build_list.py / select_tiers.py so the numbers follow the data.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import select_tiers as st  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
INDEX = ROOT / "research/companies/tiktok/index.json"
VAULTS = [ROOT / "vault/interviews/core/leetcode/tiktok/cards", ROOT / "vault/interviews/core/leetcode/tiktok-drill/cards"]
HEADER = re.compile(r"^(\*\*[^*\n]+\*\*)｜([^\n]*)$", re.M)
DIFF = re.compile(r"^(Easy|Medium|Hard|简单|中等|困难)")
WINDOW = {"30d": "近 30 天", "3m": "近 3 个月", "6m": "近 6 个月"}


def facts(index: dict[str, dict], today: date) -> dict[str, dict]:
    by_id: dict[int, list[str]] = {}
    for slug, p in index.items():
        if p.get("id"):
            by_id.setdefault(p["id"], []).append(slug)
    cut = today - timedelta(days=365)
    seen: dict[str, dict] = {}
    for fam in st.families():
        recent = [(d, r) for d, r in zip(fam["dates"], fam["regions"]) if st.day(d) >= cut]
        if not recent:
            continue
        dates = [d for d, _ in recent]
        slugs = [s for n in fam["lc"] for s in by_id.get(n, [])]
        v = next((v for k, v in st.FAMILY_VARIANT.items() if fam["family"].startswith(k)), None)
        if v and v in index:
            slugs.append(v)
        for s in slugs:
            f = seen.setdefault(s, {"n": 0, "us": 0, "cn": 0, "last": ""})
            f["n"] += len(dates)
            f["us"] += sum(1 for _, r in recent if r == "US")
            f["cn"] += sum(1 for _, r in recent if r == "CN")
            f["last"] = max([f["last"], *dates], key=st.day)
    snap = {r["slug"]: r for r in json.loads((st.CAT / "codetop.json").read_text(encoding="utf-8"))["rows"]}
    out = {}
    for slug, p in index.items():
        parts, last = [], []
        for key, label in (("tiktok", "TikTok"), ("bytedance", "字节")):
            if key in p["companies"]:
                parts.append(f"LC {label} 热度 {p['companies'][key]['freq']}/100"
                             + (f"（{WINDOW[p['window']]}）" if p.get("window") in WINDOW else ""))
                break
        if slug in seen:
            parts.append(f"近一年被问：美国 {seen[slug]['us']} 次、国内 {seen[slug]['cn']} 次")
            last.append((seen[slug]["last"], "面试记录"))
        ct = snap.get(slug) or ({"reports": p["companies"]["bytedance_cn"]["reports"],
                                 "last_seen": p["companies"]["bytedance_cn"]["last_seen"]}
                                if "bytedance_cn" in p["companies"] else None)
        if ct:
            parts.append(f"CodeTop 国内累计 {ct['reports']} 次")
            last.append((ct["last_seen"], "CodeTop"))
        if last:
            d, src = max(last, key=lambda x: (st.day(x[0]), len(x[0])))
            parts.append(f"最近 {d}（{src}）")
        out[slug] = {"stats": " · ".join(parts) or "TikTok 高频", "difficulty": p.get("difficulty") or ""}
    return out


def main(argv: list[str]) -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    info = facts(index, date.today())
    changed = 0
    for vault in VAULTS:
        for f in sorted(vault.glob("[ab]/tlc-*.md")):
            text = f.read_text(encoding="utf-8")
            node = re.search(r"^node: [ab]\.(\S+)$", text, re.M)
            if not node or node.group(1) not in info or not ("-0-whole" in f.name or "-1-signal" in f.name):
                continue
            q = text.split("## A", 1)
            m = HEADER.search(q[0])
            if not m:
                continue
            old = m.group(2)
            d = DIFF.match(old)
            diff = d.group(1) if d else info[node.group(1)]["difficulty"]
            meta = " · ".join(x for x in (diff, info[node.group(1)]["stats"]) if x)
            if meta == old:
                continue
            q[0] = q[0][:m.start(2)] + meta + q[0][m.end(2):]
            changed += 1
            if "--dry-run" in argv:
                if changed <= 8:
                    print(f.name, "|", old, "->", meta)
                continue
            f.write_text("## A".join(q), encoding="utf-8")
    print(changed, "headers", "would change" if "--dry-run" in argv else "updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
