"""One file per LeetCode problem, shared by every deck that has a whole-answer card for it.

    uv run python scripts/lc_problems.py migrate     # once: move card bodies into problems/, turn deck cards into stubs
    uv run python scripts/lc_problems.py stub <deck card path> <slug> [--meta "..."]   # write one stub
    uv run python scripts/lc_problems.py where <slug>                                 # which decks use a problem

`vault/interviews/core/leetcode/problems/<slug>.md` holds the statement and the answer (the single source of truth;
edit there). A deck card is a stub: its own `id` and `node` (so each deck keeps its own Anki schedule), `body:` pointing
to the shared file, and `meta:` for the deck's header facts (difficulty, frequency, lists). Split cards (deck 25) and
pattern / toolkit cards are not problem bodies and stay as they are.

Which version became the shared body when two decks had different text: the TikTok card for TikTok tier A problems and
TikTok variants (what Chi drilled before his interview), else the LeetCode Tops card (written to the newest rules),
else whichever exists.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LC = ROOT / "vault/interviews/core/leetcode"
PROBLEMS = LC / "problems"
DECKS = {  # deck folder -> (glob, slug from file name)
    "tiktok": ("tiktok/cards/*/tlc-*-0-whole.md", re.compile(r"^tlc-(.+)-0-whole$")),
    "tops": ("tops/cards/*/tlc-tops-*-0-whole.md", re.compile(r"^tlc-tops-(.+)-0-whole$")),
    "daily": ("daily/cards/tlc-daily-*-0-whole.md", re.compile(r"^tlc-daily-(.+)-0-whole$")),
    "core": ("tiktok-core/cards/*/tlc-core-*.md", re.compile(r"^tlc-core-(.+)$")),
}
HEADER = re.compile(r"^(\*\*[^*\n]+\*\*)｜(.*)$", re.M)
FRONT = re.compile(r"^---\n(.*?)\n---\n", re.S)


def split(text: str) -> tuple[str, str]:
    m = FRONT.match(text)
    return (m.group(1), text[m.end():]) if m else ("", text)


def cards() -> dict[str, dict[str, Path]]:
    out: dict[str, dict[str, Path]] = {}
    for deck, (pattern, rx) in DECKS.items():
        for f in sorted(LC.glob(pattern)):
            m = rx.match(f.stem)
            if m:
                out.setdefault(m.group(1), {})[deck] = f
    return out


def stub(path: Path, slug: str, header_meta: str) -> None:
    front, _ = split(path.read_text(encoding="utf-8"))
    keep = [l for l in front.splitlines() if not l.startswith(("body:", "meta:"))]
    meta_line = f"meta: {json.dumps(header_meta, ensure_ascii=False)}" if header_meta else ""
    lines = keep + [f"body: interviews/core/leetcode/problems/{slug}"] + ([meta_line] if meta_line else [])
    path.write_text("---\n" + "\n".join(lines) + "\n---\n", encoding="utf-8")


def migrate() -> int:
    index = json.loads((ROOT / "research/companies/tiktok/index.json").read_text(encoding="utf-8"))
    PROBLEMS.mkdir(parents=True, exist_ok=True)
    made = stubs = 0
    for slug, where in sorted(cards().items()):
        band = index.get(slug, {}).get("band", "")
        order = ["tiktok", "tops", "daily", "core"] if (band.startswith("p") or slug.startswith("tt-")) \
            else ["tops", "tiktok", "daily", "core"]
        src = next(where[d] for d in order if d in where)
        dest = PROBLEMS / f"{slug}.md"
        if not dest.exists():
            front, body = split(src.read_text(encoding="utf-8"))
            if front and "body:" in front:
                continue  # already a stub
            h = HEADER.search(body)
            diff = re.match(r"(Easy|Medium|Hard)", h.group(2)) if h else None
            if h:  # the shared header carries only the difficulty; decks add their facts through meta
                body = body[:h.start(2)] + (diff.group(1) if diff else "") + body[h.end(2):]
            dest.write_text(f"---\nslug: {slug}\n---\n" + body, encoding="utf-8")
            made += 1
        for deck, f in where.items():
            front, body = split(f.read_text(encoding="utf-8"))
            if "body:" in front:
                continue
            h = HEADER.search(body)
            stub(f, slug, h.group(2).strip() if h else "")
            stubs += 1
    print(made, "shared problem files;", stubs, "deck cards turned into stubs")
    return 0


def where(slug: str) -> int:
    for deck, f in cards().get(slug, {}).items():
        print(deck, f.relative_to(ROOT))
    print("shared:", (PROBLEMS / f"{slug}.md").relative_to(ROOT), "exists" if (PROBLEMS / f"{slug}.md").exists() else "missing")
    return 0


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "migrate":
        sys.exit(migrate())
    if cmd == "where":
        sys.exit(where(args[0]))
    if cmd == "stub":
        m = args.index("--meta") if "--meta" in args else None
        stub(Path(args[0]), args[1], args[m + 1] if m is not None else "")
        sys.exit(0)
