"""重生成 study/30-articles/README.md（文章 → 题目目录 → 最值得带走的一个模式）。

  trellis kit articles_readme --co abnormal
  trellis kit articles_readme --co millennium      # 档案里把所有文章钉在 01_first_round（--round-dir / --round-label）

默认在 loop/rounds/*/ 下按文章名找题目目录，轮次列写目录所在轮次；给 --round-dir 就不找，直接按该轮次目录写。
"""
from __future__ import annotations

import argparse
import re

from .paths import Kit


def add_arguments(ap: argparse.ArgumentParser, common: argparse.ArgumentParser) -> None:
    ap.add_argument("--round-dir", default=None, help="把所有文章钉在这个 loop/rounds/ 子目录（默认取该公司档案，空 = 自动找）")
    ap.add_argument("--round-label", default=None, help="钉死轮次目录时，轮次列写什么")


def run(a, kit: Kit) -> int:
    root = kit.kit
    round_dir = kit.profile.articles_round_dir if a.round_dir is None else a.round_dir
    round_label = a.round_label if a.round_label is not None else kit.profile.articles_round_label
    arts = sorted((root / "study" / "30-articles").glob("pc*.md"))
    rows = []
    for art in arts:
        m = re.search(r"最值得带走的一个模式[：:]\s*(.+)", art.read_text(encoding="utf-8"))
        pat = (m.group(1).strip() if m else "").rstrip("。")
        if round_dir:
            rows.append(f"| [{art.stem}]({art.name}) | `../../loop/rounds/{round_dir}/{art.stem}/` | {round_label} | {pat[:120]} |")
            continue
        d = next((root / "loop" / "rounds").glob(f"*/{art.stem}"), None)
        rel = f"../../{d.relative_to(root).as_posix()}/" if d else "—"
        rows.append(f"| [{art.stem}]({art.name}) | `{rel}` | {d.parent.name if d else '—'} | {pat[:120]} |")
    head = ("# study/30-articles — 每题一篇中文题解\n\n> **先做题再读**：题解是验收用的，不是读着爽的。格式见 `_TEMPLATE.md`；"
            "每篇的代码骨架与该题 `solution.py` 一致（简化，不矛盾）。本表由 `trellis kit articles_readme` 生成，勿手改。\n\n"
            "| 文章 | 题目目录 | 轮次 | 最值得带走的一个模式 |\n|---|---|---|---|\n")
    (root / "study" / "30-articles" / "README.md").write_text(head + "\n".join(rows) + "\n", encoding="utf-8")
    print(len(rows))
    return 0
