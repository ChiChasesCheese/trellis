"""The next cards to give a diagram to, in the order Chi will meet them (Chi, 2026-11-14: backfill old decks on a schedule).

    uv run python scripts/diagram_queue.py -n 40 -o sources/local/plan/diagram_queue.txt
    uv run python scripts/diagram_queue.py --skip <card id> …      # judged not worth a picture: never queued again

Order: new and learning cards in his daily decks (今日计划, 今日算法, 今日低层设计, 系统设计高频题, the sprint deck), by
the position Anki deals them in; then the rest of each domain still under the 25% floor, lowest share first. A card
already holding a diagram, or on the skip list, is left out. Output: one card file path per line (repo-relative).
The writing rules are research/agents/DIAGRAM_BACKFILL_TASK.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SKIP = ROOT / "sources/local/plan/diagram_skip.txt"
DIAGRAM = re.compile(r"^```(?:mermaid|svg)\b|!\[\[[^\]]+\.(?:png|jpe?g|svg|gif|webp)\]\]|!\[[^\]]*\]\([^)]+\)", re.M)
FLOOR = 0.25
NO_DIAGRAMS = {"basketball"}  # video clips carry these cards
# among domains equally far below the floor, the ones he studies most come first
STUDIED = ["hello-interview", "low-level-design", "leetcode-tree", "python", "code-core", "narrative", "pl", "kafka", "payments",
           "hft", "snowflake", "cdn-content", "stripe", "headlands", "system-design", "leetcode", "tiktok-lc", "tiktok-lc-drill"]


def index() -> tuple[dict[str, Path], dict[str, list[str]], dict[str, float]]:
    """card id -> file; domain -> its card ids without a diagram; domain -> diagram share."""
    files, bare, share = {}, {}, {}
    for f in sorted((ROOT / "skeleton").glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(d, dict) or not d.get("vault") or d.get("domain") in ("sysdesign",):
            continue  # sysdesign is a view over other domains' folders
        base = ROOT / "vault" / d["vault"]
        n = fig = 0
        missing = []
        for p in base.rglob("*.md"):
            t = p.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^id: (\S+)", t[:400], re.M)
            if not (t.startswith("---") and m and "## A" in t):
                continue
            files[m.group(1)] = p
            n += 1
            if DIAGRAM.search(t):
                fig += 1
            else:
                missing.append(m.group(1))
        if n:
            bare[d["domain"]], share[d["domain"]] = missing, fig / n
    return files, bare, share


def studied_next() -> list[str]:
    """Card ids in the daily decks, new or learning, in dealing order."""
    import company_deck
    import daily_extra
    from anki_refresh import call
    decks = list(daily_extra.DAILY) + company_deck.decks()
    q = "(" + " OR ".join(company_deck.in_deck(d) for d in decks) + ") (is:new OR is:learn) -is:suspended"
    cids = call("findCards", query=q)
    info = []
    for i in range(0, len(cids), 500):
        info += call("cardsInfo", cards=cids[i:i + 500])
    nids = sorted({c["note"] for c in info})
    tag = {}
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            tag[n["noteId"]] = next((t[4:] for t in n["tags"] if t.startswith("id::")), "")
    info.sort(key=lambda c: (c["queue"] != 1, c["deckName"], c["due"]))  # learning first, then deck order and position
    return list(dict.fromkeys(tag[c["note"]] for c in info if tag.get(c["note"])))


def main() -> int:
    a = sys.argv[1:]
    if a[:1] == ["--skip"]:
        SKIP.parent.mkdir(parents=True, exist_ok=True)
        with SKIP.open("a", encoding="utf-8") as f:
            f.write("".join(i + "\n" for i in a[1:]))
        return 0
    n = int(a[a.index("-n") + 1]) if "-n" in a else 40
    skip = set(SKIP.read_text(encoding="utf-8").split()) if SKIP.exists() else set()
    files, bare, share = index()
    missing = {i for v in bare.values() for i in v}
    picked: list[str] = []
    for i in studied_next():
        if i in missing and i not in skip and i not in picked:
            picked.append(i)
    rank = {d: i for i, d in enumerate(STUDIED)}
    for dom in sorted((d for d in bare if share[d] < FLOOR and d not in NO_DIAGRAMS),
                      key=lambda d: (round(share[d], 1), rank.get(d, len(rank)))):
        picked += [i for i in bare[dom] if i not in skip and i not in picked]
    lines = [str(files[i].relative_to(ROOT)) for i in picked[:n]]
    if "-o" in a:
        out = ROOT / a[a.index("-o") + 1]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"# {len(lines)} queued; domains under 25%: " + ", ".join(f"{d} {share[d]:.0%}" for d in sorted(share, key=share.get) if share[d] < FLOOR),
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
