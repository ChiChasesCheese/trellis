"""覆盖率：已建题目覆盖了多少"流出题目出现次数"。

  trellis kit coverage --co millennium     # 读 catalog/RANK.md（研究目录），按轮次与总体输出

口径（写死，改了要同步 reports/OVERALL_REPORT.md）：
  * 分母 = RANK.md 每行的 #refs 之和（独立来源数 = 被报道的次数）
  * 分子 = 已有题目目录的行的 #refs 之和（kit 里的 problems/qNN_*、loop/rounds/*/<id>_*）
  * 另给"题族覆盖"：已建行数 / 总行数
  * 非编码轮（recruiter / expertise / HM / team）是题库而不是单题，不在 RANK.md 里，单独报告题库规模
这个数字只衡量"公开流出的题"。没有被报道过的新题它看不到——那部分靠 study/00-essentials 的模式迁移。

轮次名（ID 前缀 → 标签，也是输出顺序）是公司档案的一部分；--label "pc=第一轮 coding" 可改单个标签，
--labels 整张替换（"cb=AI screen,sd=系统设计"）。
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from .paths import Kit


def built_ids(root: Path) -> set[str]:
    ids = set()
    for p in (root / "problems").glob("q*_*"):
        ids.add(p.name.split("_", 1)[0])
    for p in (root / "loop" / "rounds").glob("*/*_*"):
        if p.is_dir():
            ids.add(p.name.split("_", 1)[0])
    return ids


def rows(rank: Path, prefixes: list[str]):
    id_re = re.compile(rf"^({'|'.join(prefixes)})\d+$")
    for line in rank.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not id_re.match(cells[0]):
            continue
        yield cells[0], cells[1], cells[2], int(re.search(r"\d+", cells[4]).group())


def _pairs(spec: str) -> dict[str, str]:
    return dict(item.split("=", 1) for item in spec.split(",") if "=" in item)


def add_arguments(ap: argparse.ArgumentParser, common: argparse.ArgumentParser) -> None:
    ap.add_argument("--labels", default=None, help="ID 前缀=标签,…（整张替换，顺序即输出顺序）")
    ap.add_argument("--label", action="append", default=[], metavar="PREFIX=LABEL", help="改单个标签，可重复")


def run(a, kit: Kit) -> int:
    labels = _pairs(a.labels) if a.labels else dict(kit.profile.coverage_labels)
    for item in a.label:
        labels.update(_pairs(item))
    built = built_ids(kit.kit)
    by = defaultdict(lambda: [0, 0, 0, 0])  # refs_built, refs_total, rows_built, rows_total
    missing = []
    for pid, title, _stage, refs in rows(kit.research / "catalog" / "RANK.md", list(labels)):
        b = by[labels[re.match(r"[a-z]+", pid).group()]]
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
    for k in labels.values():
        rb, rt, nb, nt = by[k]
        if rt == 0:
            continue
        print(f"| {k} | {rb}/{rt} = {rb / rt:.0%} | {nb}/{nt} |")
    print(f"| **合计** | **{tot[0]}/{tot[1]} = {tot[0] / tot[1]:.0%}** | **{tot[2]}/{tot[3]}** |")
    print("\n未建（按出现次数降序）：")
    for refs, pid, title in sorted(missing, reverse=True):
        print(f"- {pid}（{refs}）{title}")
    banks = {}
    for b in (kit.kit / "loop" / "rounds").glob("*/bank.json"):
        banks[b.parent.name] = len(json.loads(b.read_text(encoding="utf-8")))
    print("\n非编码轮题库：" + " · ".join(f"{k} {v}" for k, v in sorted(banks.items())))
    return 0
