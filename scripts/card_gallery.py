"""One HTML page of sample cards, grouped, phone-width, rendered with the real Anki build's HTML and CSS.

    uv run python scripts/card_gallery.py -o sources/local/plan/new-deck-samples.html --title "新卡组样卡" \\
        --group "Kubernetes|先修 → 摘要 → 考点 → 2026 拓展" a.md b.md \\
        --group "AI 应用工程|摘要 → 考点 → 实践" c.md
    ... --shot /tmp/gallery.png     # also screenshot it at 430 px with the installed Google Chrome (playwright)

Cards are vault-style markdown (frontmatter `node:`, then `## Q` / `## A`). Each card shows its question with the
answer folded behind 「看答案」; a group's cards scroll sideways. Mermaid blocks become SVG through the same
cached renderer the deck uses. Pages written under sources/local/plan/ are served on the tailnet by the study map
(http://100.107.177.18:8798/<name>.html). Built 2026-11-21 for Chi's sample reviews; reuse it for any new deck.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trellis import build  # noqa: E402

PAGE_CSS = """
body.page{background:#e2e8f0;margin:0;padding:12px;font-family:-apple-system,'PingFang SC',sans-serif}
.page h1{font-size:22px}.page h2{margin:22px 0 2px}.sub{color:#475569;margin:0 0 8px}
.row{display:flex;gap:14px;overflow-x:auto;align-items:flex-start;padding-bottom:8px}
.phone{flex:0 0 390px;max-width:92vw;background:#fff;border-radius:18px;box-shadow:0 2px 8px #0002;padding:4px 0}
.phone .card{margin:0}.phone details>summary{cursor:pointer;color:#2563eb;padding:6px 12px;font-weight:600}
"""


def card_html(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    q = re.search(r"^## Q\n(.*?)^## A\n", text, re.S | re.M)
    if not q:
        raise SystemExit(f"{path}: no '## Q' / '## A' sections")
    a = text.split("\n## A\n", 1)[1]
    node = (re.search(r"^node: (\S+)", text, re.M) or [None, ""])[1]
    return (f'<div class="phone"><div class="card"><div class="crumb">{node}</div>{build._html(q.group(1))}'
            f'<details><summary>看答案</summary><hr id="answer">{build._html(a, fold=False, links={}, node=node)}'
            f'</details></div></div>')


def parse_groups(argv: list[str]) -> list[tuple[str, str, list[Path]]]:
    groups: list[tuple[str, str, list[Path]]] = []
    i = 0
    while i < len(argv):
        if argv[i] != "--group":
            raise SystemExit(f"expected --group, got {argv[i]!r}")
        title, _, sub = argv[i + 1].partition("|")
        files: list[Path] = []
        i += 2
        while i < len(argv) and argv[i] != "--group":
            files.append(Path(argv[i]))
            i += 1
        groups.append((title, sub, files))
    return groups


def screenshot(page: Path, png: Path) -> None:
    from playwright.sync_api import sync_playwright  # run with: uv run --with playwright ...
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        tab = browser.new_page(viewport={"width": 430, "height": 1400}, device_scale_factor=2)
        tab.goto(page.resolve().as_uri())
        tab.evaluate("document.querySelectorAll('details').forEach(e => e.open = true)")
        tab.screenshot(path=str(png))
        browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-o", "--out", required=True, type=Path)
    ap.add_argument("--title", default="样卡")
    ap.add_argument("--intro", default="每张卡先看题，点「看答案」展开。左右滑动看同一组的其他卡。")
    ap.add_argument("--shot", type=Path, help="also save a phone-width screenshot (needs playwright + Google Chrome)")
    args, rest = ap.parse_known_args()
    groups = parse_groups(rest)
    if not groups:
        raise SystemExit("give at least one --group 'Title|subtitle' card.md ...")
    sections, total = [], 0
    for title, sub, files in groups:
        total += len(files)
        sections.append(f'<h2>{title}</h2><p class="sub">{sub}</p>'
                        f'<div class="row">{"".join(card_html(f) for f in files)}</div>')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        f'<!doctype html><html lang="zh"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{args.title}</title>'
        f'<style>{build.CSS}{PAGE_CSS}</style></head><body class="page"><h1>{args.title} · {total} 张</h1>'
        f'<p class="sub">{args.intro}</p>{"".join(sections)}</body></html>', encoding="utf-8")
    print(args.out, total, "cards")
    if args.shot:
        screenshot(args.out, args.shot)
        print(args.shot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
