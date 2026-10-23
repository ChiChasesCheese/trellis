#!/usr/bin/env python3
"""把 loop/study/30-articles/*.md 同步到 Obsidian vault 的 Inbox/Stripe Loop/，并维护索引。

  python3 loop/study/30-articles/sync_obsidian.py            # 写入 vault
  python3 loop/study/30-articles/sync_obsidian.py --dry-run  # 只打印

规则（obsidian-handoff skill）：只写 Inbox/；frontmatter 沿用 Inbox Template + claude/handoff；索引 `Claude 接力.md` 顶部加链接。
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOOP = HERE.parents[1]
VAULT = Path("/Users/chizhang/Documents/Chi")
DEST = VAULT / "Inbox" / "Stripe Loop"
INDEX_NOTE = DEST / "Stripe Loop 题解索引.md"
HANDOFF = VAULT / "Claude 接力.md"
TODAY = dt.date.today().isoformat()
ROUND_OF = {
    "ps": "电面",
    "cd": "Onsite Coding",
    "bs": "Bug Squash",
    "int": "Integration",
    "sd": "System Design",
}


def note_name(path: Path) -> str:
    """ps01_transaction_stream_levels.md → 'ps01 Transaction Stream Levels'（取文章 H1 的题名）"""
    h1 = next((ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.startswith("# ")), "")
    m = re.match(r"# (\w+) · ([^：:]+)", h1)
    pid = path.stem.split("_", 1)[0]
    title = m.group(2).strip() if m else path.stem.split("_", 1)[1].replace("_", " ")
    title = re.sub(r'[\\/:*?"<>|]', " ", title).strip()
    return f"{pid} {title}"


def frontmatter(pid: str, title: str) -> str:
    rnd = ROUND_OF.get(re.match(r"[a-z]+", pid).group(0), "loop")
    return (
        f"---\ncreated: {TODAY}\ntags:\n  - inbox\n  - claude/handoff\n  - stripe/loop\nsource: claude-code\n"
        f"topics:\n  - Stripe 面试\n  - {rnd}\n  - {pid}\n---\n\n"
    )


def tracked_articles(here: Path) -> list[Path]:
    """只取 git 已跟踪的文章（未提交 = 未验收）。"""
    import subprocess

    out = subprocess.run(
        ["git", "ls-files", "--", str(here)], capture_output=True, text=True, cwd=str(here)
    ).stdout
    names = {Path(p).name for p in out.split()}
    return sorted(p for p in here.glob("*.md") if not p.name.startswith("_") and p.name in names)


def main() -> int:
    dry = "--dry-run" in sys.argv
    articles = tracked_articles(HERE)
    if not dry:
        DEST.mkdir(parents=True, exist_ok=True)
    written = []
    for a in articles:
        name = note_name(a)
        pid = a.stem.split("_", 1)[0]
        body = a.read_text(encoding="utf-8").rstrip() + "\n\n## 回信\n\n<!-- 你写在这里，下次我会读 -->\n"
        body += f"\n<!-- source: loop/study/30-articles/{a.name} -->\n"
        target = DEST / f"{name}.md"
        print(("would write " if dry else "write ") + str(target))
        if not dry:
            target.write_text(frontmatter(pid, name) + body, encoding="utf-8")
        written.append((pid, name))
    # 索引笔记
    lines = [f"- [[{n}]]" for _, n in written]
    idx = (
        f"---\ncreated: {TODAY}\ntags:\n  - inbox\n  - claude/handoff\n  - stripe/loop\nsource: claude-code\ntopics:\n  - Stripe 面试\n---\n\n"
        "# Stripe Loop 题解索引\n\n> [!tldr]\n> OA 之后各轮（电面 / onsite coding / bug squash / integration）每题一篇方法论文章：怎么读题建模、怎么下笔、怎么组织代码。"
        "不讲 corner case。练习目录在仓库 `loop/rounds/`，`python3 loop/mock.py start <id>` 计时演练。\n\n"
        f"共 {len(written)} 篇（{TODAY}）。\n\n"
        + "\n".join(lines)
        + "\n\n## 回信\n\n<!-- 你写在这里，下次我会读 -->\n"
    )
    print(("would write " if dry else "write ") + str(INDEX_NOTE))
    if not dry:
        INDEX_NOTE.write_text(idx, encoding="utf-8")
        # Claude 接力.md 顶部链接（幂等）
        link = "- [[Stripe Loop 题解索引]]"
        if HANDOFF.exists():
            txt = HANDOFF.read_text(encoding="utf-8")
            if link not in txt:
                anchor = "## 笔记"
                if anchor in txt:
                    txt = txt.replace(anchor, f"{anchor}\n\n{link}（{TODAY}）", 1)
                else:
                    txt = txt.rstrip() + f"\n\n## 笔记\n\n{link}（{TODAY}）\n"
                HANDOFF.write_text(txt, encoding="utf-8")
                print("updated " + str(HANDOFF))
    return 0


if __name__ == "__main__":
    sys.exit(main())
