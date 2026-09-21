#!/usr/bin/env python3
"""覆盖率：已建题目覆盖了多少"流出题目出现次数"。

  python3 tools/coverage.py            # 读 catalog/RANK.md，按轮次与总体输出

口径（写死，改了要同步 reports/OVERALL_REPORT.md）：
  * 分母 = RANK.md 每行的 #refs 之和（独立来源数 = 被报道的次数）
  * 分子 = 已有题目目录的行的 #refs 之和（problems/qNN_*、loop/rounds/*/<id>_*）
  * 另给"题族覆盖"：已建行数 / 总行数
  * 非编码轮（recruiter / expertise / HM / team）是题库而不是单题，不在 RANK.md 里，单独报告题库规模
这个数字只衡量"公开流出的题"。没有被报道过的新题它看不到——那部分靠 study/00-essentials 的模式迁移。
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]


def built_ids() -> set[str]:
    ids = set()
    for p in (KIT / "problems").glob("q*_*"):
        ids.add(p.name.split("_", 1)[0])
    for p in (KIT / "loop" / "rounds").glob("*/*_*"):
        if p.is_dir():
            ids.add(p.name.split("_", 1)[0])
    return ids


def rows():
    text = (KIT / "catalog" / "RANK.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not re.match(r"^(q|pc|od|sd)\d+$", cells[0]):
            continue
        yield cells[0], cells[1], cells[2], int(re.search(r"\d+", cells[4]).group())


def bucket(pid: str) -> str:
    return {"q": "OA", "pc": "第一轮 coding", "od": "OOD", "sd": "系统设计"}[re.match(r"[a-z]+", pid).group()]


def main() -> None:
    built = built_ids()
    by = defaultdict(lambda: [0, 0, 0, 0])  # refs_built, refs_total, rows_built, rows_total
    missing = []
    for pid, title, _stage, refs in rows():
        b = by[bucket(pid)]
        b[1] += refs
        b[3] += 1
        if pid in built:
            b[0] += refs
            b[2] += 1
        else:
            missing.append((refs, pid, title[:60]))
    tot = [sum(v[i] for v in by.values()) for i in range(4)]
    print("| 轮次 | 出现次数覆盖 | 题族覆盖 |")
    print("|---|---:|---:|")
    for k in ("OA", "第一轮 coding", "OOD", "系统设计"):
        rb, rt, nb, nt = by[k]
        if rt == 0:
            continue
        print(f"| {k} | {rb}/{rt} = {rb / rt:.0%} | {nb}/{nt} |")
    print(f"| **合计** | **{tot[0]}/{tot[1]} = {tot[0] / tot[1]:.0%}** | **{tot[2]}/{tot[3]}** |")
    print("\n未建（按出现次数降序）：")
    for refs, pid, title in sorted(missing, reverse=True):
        print(f"- {pid}（{refs}）{title}")
    import json
    banks = {}
    for b in (KIT / "loop" / "rounds").glob("*/bank.json"):
        banks[b.parent.name] = len(json.loads(b.read_text(encoding="utf-8")))
    print("\n非编码轮题库：" + " · ".join(f"{k} {v}" for k, v in sorted(banks.items())))


if __name__ == "__main__":
    main()
