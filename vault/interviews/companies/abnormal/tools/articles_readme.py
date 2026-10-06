#!/usr/bin/env python3
"""重生成 study/30-articles/README.md（文章 → 题目目录 → 最值得带走的一个模式）。"""
import pathlib, re
KIT = pathlib.Path(__file__).resolve().parents[1]
arts = sorted((KIT / "study" / "30-articles").glob("pc*.md"))
rows = []
for a in arts:
    m = re.search(r"最值得带走的一个模式[：:]\s*(.+)", a.read_text(encoding="utf-8"))
    pat = (m.group(1).strip() if m else "").rstrip("。")
    rows.append(f"| [{a.stem}]({a.name}) | `../../loop/rounds/01_first_round/{a.stem}/` | R1 coding | {pat[:120]} |")
head = ("# study/30-articles — 每题一篇中文题解\n\n> **先做题再读**：题解是验收用的，不是读着爽的。格式见 `_TEMPLATE.md`；"
        "每篇的代码骨架与该题 `solution.py` 一致（简化，不矛盾）。本表由 `tools/articles_readme.py` 生成，勿手改。\n\n"
        "| 文章 | 题目目录 | 轮次 | 最值得带走的一个模式 |\n|---|---|---|---|\n")
(KIT / "study" / "30-articles" / "README.md").write_text(head + "\n".join(rows) + "\n", encoding="utf-8")
print(len(rows))
