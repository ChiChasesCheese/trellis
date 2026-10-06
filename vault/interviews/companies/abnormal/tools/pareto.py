#!/usr/bin/env python3
"""28 法则排序：读 CATALOG.md 里的一张 markdown 表，按 轮次权重 × #refs × 时效 打分，
打印排序后的行、累计覆盖率，以及"覆盖 80% 出现次数"的 cut line。

  python3 tools/pareto.py catalog/CATALOG.md --table "Table A"          # 默认列名见下
  python3 tools/pareto.py catalog/TALLY.md --refs-col "#refs" --date-col "最近" --stage-col "轮次"

规则（写在代码里，改了要同步改 CATALOG 的说明块）：
  * refs   = 独立来源数（同一候选人跨站算 1；聚合站互抄算 1）
  * 时效   = 最近一次报道距今：≤3 个月 1.0 · ≤12 个月 0.8 · ≤24 个月 0.6 · 更早 0.4 · 无日期 0.5
  * 轮次权重 = 当前要面的轮次 1.0（--focus，默认 OA/电面）· 其它技术轮 0.8 · 非编码轮 0.6
  * score  = refs × 时效 × 轮次权重；cut line = 累计 score 首次 ≥ 80% 的行
表格列名不区分大小写；日期取行里第一个 YYYY-MM 或 YYYY-MM-DD。
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"(20\d{2})-(\d{2})(?:-(\d{2}))?")


def load_table(path: Path, table: str | None) -> tuple[list[str], list[list[str]]]:
    text = path.read_text(encoding="utf-8")
    if table:
        m = re.search(rf"^#+ [^\n]*{re.escape(table)}[^\n]*$(.*?)(?=^#+ |\Z)", text, re.S | re.M)
        if not m:
            sys.exit(f"没有找到标题包含 {table!r} 的小节")
        text = m.group(1)
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("|")]
    if len(rows) < 3:
        sys.exit("表格行数不足（需要表头 + 分隔线 + 至少一行）")
    cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:] if set(r.strip()) - set("|-: ")]
    return head, body


def col(head: list[str], name: str) -> int:
    for i, h in enumerate(head):
        if h.lower().replace("*", "") == name.lower():
            return i
    for i, h in enumerate(head):
        if name.lower() in h.lower():
            return i
    sys.exit(f"表头里没有列 {name!r}；表头是 {head}")


def recency(s: str, today: dt.date) -> float:
    m = DATE_RE.search(s)
    if not m:
        return 0.5
    y, mo = int(m.group(1)), int(m.group(2))
    months = (today.year - y) * 12 + (today.month - mo)
    return 1.0 if months <= 3 else 0.8 if months <= 12 else 0.6 if months <= 24 else 0.4


def stage_weight(s: str, focus: list[str]) -> float:
    s_low = s.lower()
    if any(f.lower() in s_low for f in focus):
        return 1.0
    if any(k in s_low for k in ("recruiter", "hm", "behavior", "bq", "team", "非编码", "hr")):
        return 0.6
    return 0.8


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=Path)
    ap.add_argument("--table", help="小节标题里的关键词，例如 'Table A'")
    ap.add_argument("--refs-col", default="#refs")
    ap.add_argument("--date-col", default="最近")
    ap.add_argument("--stage-col", default="轮次")
    ap.add_argument("--title-col", default=None, help="默认取第 2 列")
    ap.add_argument("--focus", default="OA,电面,phone", help="逗号分隔；命中这些字样的轮次权重 1.0")
    ap.add_argument("--cut", type=float, default=0.8)
    a = ap.parse_args()

    head, body = load_table(a.file, a.table)
    ir, idt, ist = col(head, a.refs_col), col(head, a.date_col), col(head, a.stage_col)
    it = col(head, a.title_col) if a.title_col else 1
    today = dt.date.today()
    focus = [f.strip() for f in a.focus.split(",") if f.strip()]

    scored = []
    for r in body:
        if len(r) <= max(ir, idt, ist, it):
            continue
        m = re.search(r"\d+", r[ir])
        refs = int(m.group()) if m else 0
        sc = refs * recency(r[idt], today) * stage_weight(r[ist], focus)
        scored.append((sc, refs, r))
    scored.sort(key=lambda x: (-x[0], -x[1]))
    total = sum(s for s, _, _ in scored) or 1.0

    print(f"| # | 题 | 轮次 | #refs | 最近 | score | 累计 |")
    print("|---|---|---|---:|---|---:|---:|")
    cum, cut_at = 0.0, None
    for i, (sc, refs, r) in enumerate(scored, 1):
        cum += sc
        share = cum / total
        if cut_at is None and share >= a.cut:
            cut_at = i
        print(f"| {i} | {r[it][:60]} | {r[ist][:24]} | {refs} | {r[idt][:16]} | {sc:.2f} | {share:.0%} |")
    n = len(scored)
    print(f"\n**{n} 行 · 累计 {a.cut:.0%} 出现在第 {cut_at} 行（前 {cut_at / n:.0%}）** —— cut line 以内的题先建题库。")


if __name__ == "__main__":
    main()
