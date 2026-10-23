#!/usr/bin/env python3
"""从 30-articles/*.md 抽卡 → Anki（AnkiConnect，牌组 Stripe::Loop::<轮次>）+ TSV 备份。

  python3 loop/study/30-articles/to_anki.py            # 写 TSV 并推送到 Anki（AnkiConnect 不可达则只写 TSV）
  python3 loop/study/30-articles/to_anki.py --dry-run  # 只打印

每篇文章 5 张卡：考什么 / 三步套路 / 最值得带走的模式 / 一句话建模 / 方法层面跑偏。幂等：按 Front 去重（allowDuplicate=false）。
"""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TSV = HERE.parents[1] / "study" / "20-cards" / "anki" / "stripe_loop.tsv"
ANKI = "http://127.0.0.1:8765"
ROUND_OF = {
    "ps": "电面",
    "cd": "Onsite Coding",
    "bs": "Bug Squash",
    "int": "Integration",
    "sd": "System Design",
}


def md_inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s


def bullets_html(lines: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{md_inline(ln)}</li>" for ln in lines) + "</ul>"


def extract(path: Path) -> list[tuple[str, str, list[str]]]:
    text = path.read_text(encoding="utf-8")
    pid = path.stem.split("_", 1)[0]
    h1 = next((ln for ln in text.splitlines() if ln.startswith("# ")), "")
    m = re.match(r"# (\w+) · ([^：:]+)", h1)
    title = m.group(2).strip() if m else path.stem
    tags = ["stripe-loop", pid, ROUND_OF.get(re.match(r"[a-z]+", pid).group(0), "loop").replace(" ", "_")]
    cards: list[tuple[str, str, list[str]]] = []
    # tldr 三条
    tldr = re.search(r"> \[!tldr\]\n((?:> .*\n?)+)", text)
    if tldr:
        items = [
            re.sub(r"^> - ", "", ln).strip() for ln in tldr.group(1).splitlines() if ln.startswith("> - ")
        ]
        labels = ["这题考的是什么？", "三步套路？", "最值得带走的一个模式？"]
        for lab, item in zip(labels, items):
            item = re.sub(r"^(这题考的是|三步套路|最值得带走的一个模式)[：:]\s*", "", item)
            cards.append((f"<b>{pid} · {md_inline(title)}</b><br>{lab}", md_inline(item), tags))
    # 一句话建模
    mm = re.search(r"\*\*一句话建模\*\*[：:]\s*(.+)", text)
    if mm:
        cards.append(
            (f"<b>{pid} · {md_inline(title)}</b><br>一句话建模？", md_inline(mm.group(1).strip()), tags)
        )
    # 第 7 节跑偏
    sec7 = re.search(r"## 7\. [^\n]*\n((?:.*\n)*?)(?=## 8\.)", text)
    if sec7:
        items = [re.sub(r"^- ", "", ln).strip() for ln in sec7.group(1).splitlines() if ln.startswith("- ")]
        if items:
            cards.append(
                (
                    f"<b>{pid} · {md_inline(title)}</b><br>方法层面最常见的 3 个跑偏？",
                    bullets_html(items[:3]),
                    tags,
                )
            )
    return cards


def anki(action: str, **params):
    req = urllib.request.Request(
        ANKI,
        data=json.dumps({"action": action, "version": 6, "params": params}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        out = json.loads(r.read())
    if out.get("error"):
        raise RuntimeError(out["error"])
    return out["result"]


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
    notes = []
    for a in articles:
        pid = a.stem.split("_", 1)[0]
        deck = "Stripe::Loop::" + ROUND_OF.get(re.match(r"[a-z]+", pid).group(0), "misc")
        for front, back, tags in extract(a):
            notes.append(
                {
                    "deckName": deck,
                    "modelName": "Basic",
                    "fields": {"Front": front, "Back": back},
                    "tags": tags,
                    "options": {"allowDuplicate": False, "duplicateScope": "deck"},
                }
            )
    print(f"{len(articles)} 篇文章 → {len(notes)} 张卡")
    TSV.parent.mkdir(parents=True, exist_ok=True)
    if not dry:
        with TSV.open("w", encoding="utf-8") as f:
            f.write("#separator:tab\n#html:true\n#deck column:3\n#tags column:4\n")
            for n in notes:
                f.write(
                    "\t".join([n["fields"]["Front"], n["fields"]["Back"], n["deckName"], " ".join(n["tags"])])
                    + "\n"
                )
        print(f"TSV → {TSV}")
    if dry:
        for n in notes[:5]:
            print(
                "-",
                re.sub("<[^>]+>", "", n["fields"]["Front"]),
                "=>",
                re.sub("<[^>]+>", "", n["fields"]["Back"])[:60],
            )
        return 0
    try:
        anki("version")
    except Exception as e:  # noqa: BLE001
        print(f"AnkiConnect 不可达（{e}），只写了 TSV；在 Anki 里 File → Import 导入即可")
        return 0
    for deck in sorted({n["deckName"] for n in notes}):
        anki("createDeck", deck=deck)
    # 幂等：先按 (deck, Front) 查找；存在 → 更新 Back；不存在 → 新增
    to_add, updated = [], 0
    for n in notes:
        front = n["fields"]["Front"].replace("\\", "\\\\").replace('"', '\\"')
        ids = anki("findNotes", query=f'"deck:{n["deckName"]}" "Front:{front}"')
        if ids:
            anki("updateNoteFields", note={"id": ids[0], "fields": {"Back": n["fields"]["Back"]}})
            updated += 1
        else:
            to_add.append(n)
    added = 0
    if to_add:
        res = anki("addNotes", notes=to_add)
        added = sum(1 for r in res if r)
    print(f"Anki：新增 {added} 张，更新 {updated} 张")
    try:
        anki("sync")
        print("AnkiWeb sync 已触发")
    except Exception as e:  # noqa: BLE001
        print(f"AnkiWeb sync 未执行：{e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
