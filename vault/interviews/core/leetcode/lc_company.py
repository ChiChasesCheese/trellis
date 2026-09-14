#!/usr/bin/env python3
"""按公司生成 LeetCode 公司标签题单（只列链接 + 标签，不写题解）。

数据源（GitHub 优先：别人整理好的，我们只蒸馏）：
  1. liquidslr/leetcode-company-wise-problems   主源：频率 + Topics，按 30天/3月/6月/更早/全部 分文件
  2. snehasishroy/leetcode-companywise-interview-questions   副源：交叉印证频率与题号

用法：
  python3 lc_company.py Snowflake              # 写 companies/snowflake.md
  python3 lc_company.py Stripe Snowflake       # 多家
  python3 lc_company.py --all-existing         # 重新生成 companies/ 下已有的所有公司

本 kit 映射（可选）：companies/<co>.kitmap.json  {"<lc-slug>": "pc06", ...}
分档：A = 近 6 个月出现 或 频率 ≥ 70；B = 频率 ≥ 50；C = 其余。
依赖：已登录的 gh CLI。
"""
import argparse
import base64
import csv
import io
import json
import pathlib
import subprocess
import sys
from collections import Counter
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "companies"
PRIMARY = "liquidslr/leetcode-company-wise-problems"
SECONDARY = "snehasishroy/leetcode-companywise-interview-questions"
P_RECENT = ["1. Thirty Days", "2. Three Months", "3. Six Months"]
S_RECENT = ["thirty-days", "three-months", "six-months"]


def gh_file(repo, path):
    p = subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}"], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return base64.b64decode(json.loads(p.stdout)["content"]).decode("utf-8", "replace")


def gh_dirs(repo):
    p = subprocess.run(["gh", "api", f"repos/{repo}/contents/", "--jq", ".[] | select(.type==\"dir\") | .name"],
                       capture_output=True, text=True)
    return p.stdout.split() if p.returncode == 0 else []


def resolve_dir(repo, company, cache={}):
    if repo not in cache:
        cache[repo] = gh_dirs(repo)
    want = company.lower().replace(" ", "").replace("-", "")
    for d in cache[repo]:
        if d.lower().replace(" ", "").replace("-", "") == want:
            return d
    return None


def rows(text):
    return list(csv.DictReader(io.StringIO(text))) if text else []


def slug(url):
    return url.rstrip("/").split("/problems/")[1].split("/")[0]


def pct(v):
    try:
        return float(str(v).rstrip("%") or 0)
    except ValueError:
        return 0.0


def build(company):
    pd, sd = resolve_dir(PRIMARY, company), resolve_dir(SECONDARY, company)
    if not pd and not sd:
        sys.exit(f"找不到公司目录：{company}（两个源都没有）")
    prim = {slug(r["Link"]): r for r in rows(gh_file(PRIMARY, f"{pd}/5. All.csv"))} if pd else {}
    prim_recent = {slug(r["Link"]) for f in P_RECENT for r in rows(gh_file(PRIMARY, f"{pd}/{f}.csv"))} if pd else set()
    sec = {slug(r["URL"]): r for r in rows(gh_file(SECONDARY, f"{sd}/all.csv"))} if sd else {}
    sec_recent = {slug(r["URL"]) for f in S_RECENT for r in rows(gh_file(SECONDARY, f"{sd}/{f}.csv"))} if sd else set()

    name = (pd or sd).lower().replace(" ", "-")
    kitmap_path = OUT / f"{name}.kitmap.json"
    kitmap = json.loads(kitmap_path.read_text()) if kitmap_path.exists() else {}

    items = []
    for s in set(prim) | set(sec):
        p, q = prim.get(s, {}), sec.get(s, {})
        freq = max(pct(p.get("Frequency")), pct(q.get("Frequency %")))
        recent = s in prim_recent or s in sec_recent
        tier = "A" if (recent or freq >= 70) else ("B" if freq >= 50 else "C")
        items.append(dict(
            slug=s, id=q.get("ID", ""), title=p.get("Title") or q.get("Title"),
            diff=(p.get("Difficulty") or q.get("Difficulty") or "").capitalize(),
            freq=freq, recent=recent, both=bool(p and q), tier=tier,
            tags=p.get("Topics", ""), kit=kitmap.get(s, "")))
    items.sort(key=lambda o: (o["tier"], -o["freq"], o["title"]))
    return name, pd or sd, items


def render(name, display, items):
    tiers = Counter(o["tier"] for o in items)
    tags = Counter(t.strip() for o in items for t in o["tags"].split(",") if t.strip())
    lines = [
        f"# {display} · LeetCode 公司标签题单",
        "",
        f"> 由 `core/leetcode/lc_company.py` 于 {date.today()} 从 GitHub 生成，**勿手改**（重跑覆盖）。"
        f"源：[{PRIMARY}](https://github.com/{PRIMARY}) · [{SECONDARY}](https://github.com/{SECONDARY})。",
        "> 频率是 LeetCode Premium 的相对值（0–100），不是出现次数；这份表只列链接与标签，题解去 LeetCode 看。",
        "",
        f"**{len(items)} 题** · A {tiers['A']} / B {tiers['B']} / C {tiers['C']} · "
        f"本 kit 已有对应 {sum(1 for o in items if o['kit'])} 题",
        "",
        "分档：**A** = 近 6 个月出现或频率 ≥ 70（先刷）· **B** = 频率 ≥ 50 · **C** = 其余（有空再刷）。"
        "`近` = 出现在 30 天 / 3 月 / 6 月 任一文件；`双源` = 两个仓库都收录。",
        "",
        "**高频标签**：" + " · ".join(f"{t} {c}" for t, c in tags.most_common(12)),
        "",
    ]
    for t in "ABC":
        group = [o for o in items if o["tier"] == t]
        if not group:
            continue
        lines += [f"## {t} 档（{len(group)}）", "", "| # | 题 | 难度 | 频率 | 近 | 双源 | 标签 | 本 kit |",
                  "|---:|---|---|---:|:-:|:-:|---|---|"]
        for o in group:
            lines.append(
                f"| {o['id']} | [{o['title']}](https://leetcode.com/problems/{o['slug']}/) | {o['diff']} | "
                f"{o['freq']:.0f} | {'✓' if o['recent'] else ''} | {'✓' if o['both'] else ''} | {o['tags']} | {o['kit']} |")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("companies", nargs="*")
    ap.add_argument("--all-existing", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    names = list(a.companies)
    if a.all_existing:
        names += [p.stem for p in OUT.glob("*.md")]
    if not names:
        ap.error("给出公司名，或 --all-existing")
    for c in dict.fromkeys(names):
        name, display, items = build(c)
        (OUT / f"{name}.md").write_text(render(name, display, items))
        print(f"{name}: {len(items)} 题 → companies/{name}.md")
    index = ["# LeetCode 公司标签题单索引", "", "每家一份，`python3 lc_company.py <Company>` 生成；映射到本仓库 kit 题号用 `companies/<co>.kitmap.json`。", ""]
    for p in sorted(OUT.glob("*.md")):
        index.append(f"- [{p.stem}](companies/{p.name})")
    (HERE / "README.md").write_text("\n".join(index) + "\n")


if __name__ == "__main__":
    main()
