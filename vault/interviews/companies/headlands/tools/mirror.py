#!/usr/bin/env python3
"""把 1p3a 镜像里的题目，标准化成本仓库的题目目录。

镜像在 `catalog/raw/mirror_1p3a_stripe/`（168 条转录，出处见那里的 README）。
这个工具负责「从镜像到题目」这条流水线的前半段：查、看、比、起骨架。
后半段（写规则、写解、写测试）仍然是人和 agent 的活——**工具不编题面**。

  python3 tools/mirror.py list [--full] [--since 20260101] [--kind coding]
  python3 tools/mirror.py show <slug 片段>
  python3 tools/mirror.py grep <关键词>
  python3 tools/mirror.py gaps              # 镜像里有、catalog 里搜不到的题名
  python3 tools/mirror.py scaffold <slug 片段> --as ps14_my_slug --round 03_phone_screen

## 三档可信度（`list` 会标出来）

- `FULL` —— 带完整题面（part 划分 / 输入输出 / 样例）。**但那是转录者的重构**，
  开头写着 "as it would be delivered by the interviewer"。题材和 part 结构可信，
  **字段名与样例数值不可当真题格式**。
- `SUMM` —— 有摘要与章节小标题（正文在付费墙后）。结构可信。
- `TITLE` —— 只有题名与日期。只能证明"这题存在过"。

`scaffold` 会按档位往 problem.md 里写不同强度的警示块——FULL 也一样要警示，
因为它不是逐字原题。
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIRROR = ROOT / "catalog" / "raw" / "mirror_1p3a_stripe"
CATALOG = ROOT / "catalog" / "CATALOG.md"
NAME_RE = re.compile(r"^(\d+)__(\d{8})__(.+?)__(oj|popular|thread)_(.+)$")


def entries() -> list[dict]:
    out = []
    for f in sorted(MIRROR.rglob("*.txt")):
        m = NAME_RE.match(f.stem)
        text = f.read_text(encoding="utf-8", errors="replace")
        src = re.search(r"^Source:\s*(.+)$", text, re.M)
        summ = re.search(r"Question Summary:\s*\n(.*?)\n\s*\n", text, re.S)
        if "INTERVIEW PROMPT" in text:
            tier = "FULL"
            # FULL 档的正文里 "- xxx" 大多是规则/约束项，不是章节。用 PART 标记当结构。
            heads = [h.strip() for h in re.findall(r"^\s*(PART\s+\d+.*)$", text, re.M | re.I)]
            if not heads:
                heads = ["（正文里没有显式 PART 标记，去原文里看结构）"]
        else:
            heads = re.findall(r"^- (.+)$", text, re.M)
            tier = "SUMM" if (summ or heads) else "TITLE"
        out.append(
            {
                "path": f,
                "kind": f.parent.name,
                "date": m.group(2) if m else "",
                "slug": m.group(3) if m else f.stem,
                "src_type": m.group(4) if m else "",
                "source": src.group(1).strip() if src else "",
                "summary": " ".join(summ.group(1).split()) if summ else "",
                "headings": heads,
                "tier": tier,
                "text": text,
            }
        )
    return out


def _find(frag: str) -> dict:
    hits = [e for e in entries() if frag.lower() in e["slug"].lower()]
    if not hits:
        sys.exit(f"没有匹配 {frag!r} 的条目；先跑 `mirror.py list` 或 `grep`")
    if len(hits) > 1:
        print(f"匹配到 {len(hits)} 条，取第一条。其余：", file=sys.stderr)
        for h in hits[1:6]:
            print(f"  {h['slug']}", file=sys.stderr)
    return hits[0]


def cmd_list(a) -> None:
    rows = entries()
    if a.full:
        rows = [e for e in rows if e["tier"] == "FULL"]
    if a.since:
        rows = [e for e in rows if e["date"] >= a.since]
    if a.kind:
        rows = [e for e in rows if e["kind"] == a.kind]
    rows.sort(key=lambda e: e["date"], reverse=True)
    for e in rows[: a.limit]:
        print(f"{e['tier']:5s} {e['date']}  {e['kind'][:6]:6s}  {e['slug'][:72]}")
    tiers = {t: sum(1 for e in rows if e["tier"] == t) for t in ("FULL", "SUMM", "TITLE")}
    print(f"\n共 {len(rows)} 条 · FULL {tiers['FULL']} · SUMM {tiers['SUMM']} · TITLE {tiers['TITLE']}")


def cmd_show(a) -> None:
    e = _find(a.slug)
    print(f"# {e['slug']}\n档位 {e['tier']} · {e['date']} · {e['kind']} · {e['source']}\n")
    print(e["text"][: a.chars])


def cmd_grep(a) -> None:
    pat = re.compile(a.pattern, re.I)
    for e in entries():
        for line in e["text"].splitlines():
            if pat.search(line):
                print(f"{e['tier']:5s} {e['date']} {e['slug'][:44]:46s} {line.strip()[:90]}")
                break


def cmd_gaps(a) -> None:
    """镜像里有、但题名关键词在 CATALOG.md 里搜不到的条目。粗筛，仍需人工判重。"""
    cat = CATALOG.read_text(encoding="utf-8").lower()
    stop = {
        "stripe", "the", "and", "with", "for", "from", "into", "part", "multi",
        "a", "an", "of", "to", "in", "on", "by", "or", "problem", "coding", "interview",
    }
    miss = []
    for e in entries():
        words = [w for w in re.split(r"[^a-z0-9]+", e["slug"].lower()) if len(w) > 3 and w not in stop]
        if not words:
            continue
        hit = sum(1 for w in words if w in cat)
        if hit / len(words) < a.threshold:
            miss.append((hit / len(words), e))
    miss.sort(key=lambda t: (t[0], t[1]["date"]))
    for score, e in miss[: a.limit]:
        print(f"{e['tier']:5s} {e['date']}  命中 {score:.0%}  {e['slug'][:70]}")
    print(f"\n{len(miss)} 条题名关键词在 CATALOG 里命中率 < {a.threshold:.0%}（粗筛，需人工判重）")


BANNER = {
    "FULL": (
        "> ⚠️ **重建题（题面来自二手转录）**：本题面基于 1point3acres 的题目转录（{src}，{date}），\n"
        "> 转录文件开头自陈是 “as it would be delivered by the interviewer” ——**是转录者的重构，\n"
        "> 不是候选人逐字记录**。题材、part 划分、考点方向可信；**输入输出格式、字段名、样例数值\n"
        "> 是本仓库定的，不要当真题格式去背。**\n"
    ),
    "SUMM": (
        "> ⚠️ **重建题**：只拿到了题目摘要与章节小标题（{src}，{date}），**正文从未公开**。\n"
        "> part 的划分与主题方向可信，**规则、输入输出格式、样例全部是本仓库自拟的**。\n"
        "> 练它是为了覆盖下面列出的 S/A 编号，**不要背格式**。\n"
    ),
    "TITLE": (
        "> ⚠️ **重建题（仅有标题）**：上游只有一个题名和日期（{src}，{date}），**没有任何正文**。\n"
        "> 规则、输入格式、输出格式、part 划分**全部是本仓库编的**。\n"
        "> 练它是为了覆盖下面列出的 S/A 编号，**不要把这里的输出格式当成真题格式**。\n"
    ),
}


def cmd_scaffold(a) -> None:
    e = _find(a.slug)
    dest = (ROOT / "loop" / "rounds" / a.round / a.as_) if a.round else (ROOT / "problems" / a.as_)
    if dest.exists():
        sys.exit(f"{dest.relative_to(ROOT)} 已存在，先删掉或换个名字")
    dest.mkdir(parents=True)
    banner = BANNER[e["tier"]].format(src=e["source"] or "1point3acres", date=e["date"])
    heads = "\n".join(f"- {h}" for h in e["headings"]) or "（上游没有给出章节结构）"
    (dest / "problem.md").write_text(
        f"# {a.as_.split('_', 1)[0]} · TODO 题名 — TODO 一句话\n\n"
        f"{banner}\n"
        f"**Type:** TODO · **Stage:** TODO · **Last asked:** {e['date'][:4]}-{e['date'][4:6]}-{e['date'][6:]}\n"
        f"**Frequency:** 1（1p3a 镜像单条）· **Confidence:** "
        f"{'medium（二手转录，非逐字）' if e['tier'] == 'FULL' else 'low（仅摘要/标题）'}\n\n"
        f"## Sources\n- {e['source']}\n"
        f"- 本仓库镜像副本：`catalog/raw/mirror_1p3a_stripe/{e['kind']}/{e['path'].name}`\n"
        f"- 抓取日 2026-09-03；镜像仓库自身 commit 日期 2026-06-01（**它也有滞后**）\n\n"
        f"## 上游给到的摘要\n{e['summary'] or '（无）'}\n\n"
        f"## 上游给到的章节结构（part 划分参考这个）\n{heads}\n\n"
        f"## Context\nTODO\n\n## Input (stdin)\nTODO\n\n## Output\nTODO\n\n"
        f"## Rules\n### Part 1\nTODO\n\n## Worked examples\nTODO\n\n"
        f"## 本题覆盖的知识点\nTODO：对照 `skills_matrix.md` 的 S/A 编号\n",
        encoding="utf-8",
    )
    for name in ("starter_template.py", "solution.py"):
        (dest / name).write_text('"""TODO"""\n', encoding="utf-8")
    shutil.copy(dest / "starter_template.py", dest / "starter.py")
    stem = a.as_.split("_", 1)[0]
    (dest / f"test_{stem}.py").write_text(
        "import pytest  # noqa: F401\n\n# TODO：每 part >=3 个测试，另加 edge/fmt/io 各 >=1、perf 1\n",
        encoding="utf-8",
    )
    (dest / "REPORT.md").write_text(
        f"# {a.as_} · REPORT\n\n## Summary\nTODO\n\n## 来源与置信度\n"
        f"档位 **{e['tier']}**（{'完整题面但是二手重构' if e['tier'] == 'FULL' else '仅摘要/标题'}）\n"
        f"- {e['source']}\n\n## 逐 part 思路\nTODO\n\n## 隐藏测试会打的坑\nTODO\n\n"
        f"## 复杂度与实测\nTODO\n\n## 测试清单\nTODO\n\n## 本题覆盖的知识点\nTODO\n\n"
        f"## 面试官会怎么追问\nTODO\n",
        encoding="utf-8",
    )
    print(f"已起骨架：{dest.relative_to(ROOT)}")
    print(f"  档位 {e['tier']} · 警示块已按档位写入 problem.md")
    print(f"  上游原文：catalog/raw/mirror_1p3a_stripe/{e['kind']}/{e['path'].name}")
    print("  下一步：填 Rules / worked examples / solution / 测试，然后跑")
    print(f"    python3 -m pytest {dest.relative_to(ROOT)}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list")
    s.add_argument("--full", action="store_true", help="只看带完整题面的")
    s.add_argument("--since", default=None, help="YYYYMMDD")
    s.add_argument("--kind", default=None, choices=["coding", "system_design"])
    s.add_argument("--limit", type=int, default=200)
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("show")
    s.add_argument("slug")
    s.add_argument("--chars", type=int, default=6000)
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("grep")
    s.add_argument("pattern")
    s.set_defaults(fn=cmd_grep)

    s = sub.add_parser("gaps")
    s.add_argument("--threshold", type=float, default=0.34)
    s.add_argument("--limit", type=int, default=60)
    s.set_defaults(fn=cmd_gaps)

    s = sub.add_parser("scaffold")
    s.add_argument("slug")
    s.add_argument("--as", dest="as_", required=True, help="目录名，如 ps14_foo 或 q42_bar")
    s.add_argument("--round", default=None, help="loop 轮次目录名；不给则建在 problems/ 下")
    s.set_defaults(fn=cmd_scaffold)

    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
