"""One card per LeetCode problem (Chi, 2026-11-14): fold every other copy of a problem into its knowledge-tree card.

    uv run --no-project --with anki==26.9.3 python -I research/leetcode-unify/migrate.py <collection.anki2> <repo> [--apply]

Run with desktop Anki closed and a backup taken. For each problem with an answer body:
- the canonical card is the tree's `lct-<slug>` (never one in the suspended archive deck);
- the copies are `tlc-tops-<slug>-0-whole`, `tlc-<slug>-0-whole`, `tlc-core-<slug>`, `tlc-daily-<slug>-0-whole`,
  `tlc-must-<slug>-0-whole`, `lca-<slug>`, `lcb-<slug>`;
- if a copy has more progress than the canonical card (longer interval, then more reviews), its scheduling is copied
  onto the canonical card; every copy's review history moves to the canonical card, so the history is kept whole;
- the copies are suspended and moved to the deck `📦 其他::待删除 · 旧 LeetCode 副本` for Chi to delete.
Without --apply it only prints what it would do.
"""
import json
import re
import sys
from pathlib import Path

from anki.collection import Collection

ARCHIVE = "LeetCode Tops::99"
TRASH = "📦 其他::待删除 · 旧 LeetCode 副本"
DONE = "📦 其他::待删除"  # copies already moved on an earlier run are skipped
COPY = [re.compile(p) for p in (r"^tlc-tops-(.+)-0-whole$", r"^tlc-daily-(.+)-0-whole$", r"^tlc-must-(.+)-0-whole$",
                                 r"^tlc-core-(.+)$", r"^tlc-(.+)-0-whole$", r"^lca-(.+)$", r"^lcb-(.+)$")]


def copy_of(ident: str, bodies: set) -> str | None:
    """The problem a copy's id names; prefixes overlap (tlc-daily-temperatures is LC 739's copy), so the slug must exist."""
    for p in COPY:
        m = p.match(ident)
        if m and m.group(1) in bodies:
            return m.group(1)
    return None


def main() -> int:
    col_path, repo = sys.argv[1], Path(sys.argv[2])
    apply = "--apply" in sys.argv
    bodies = {f.stem for f in (repo / "vault/interviews/core/leetcode/problems").glob("*.md")}
    col = Collection(col_path)
    deck_name = {d["id"]: d["name"] for d in col.decks.all()}
    canon, copies = {}, {}
    for nid in col.find_notes('"tag:id::*"'):
        note = col.get_note(nid)
        ident = next((t[4:] for t in note.tags if t.startswith("id::")), "")
        cards = [c for c in note.cards() if not deck_name.get(c.did, "").startswith(DONE)]
        if not cards:
            continue
        if ident.startswith("lct-") and not ident.startswith("lct-learn-") and ident[4:] in bodies:
            c = cards[0]
            home = deck_name.get(c.odid or c.did, "")
            if not home.startswith(ARCHIVE):
                canon[ident[4:]] = c
            continue
        slug = copy_of(ident, bodies)
        if slug:
            copies.setdefault(slug, []).extend(cards)
    trash = col.decks.id(TRASH)
    moved = transferred = merged_logs = 0
    moved_ids: list[int] = []
    no_canon = sorted(s for s in copies if s not in canon)
    for slug, cs in copies.items():
        c = canon.get(slug)
        if c is None:
            continue
        best = max([c] + cs, key=lambda x: (x.ivl, x.reps, -x.lapses))
        if best.id != c.id and best.reps > 0:
            transferred += 1
            if apply:
                for f in ("type", "queue", "due", "ivl", "factor", "reps", "lapses", "left"):
                    setattr(c, f, getattr(best, f))
                if getattr(best, "memory_state", None) is not None:
                    c.memory_state = best.memory_state
                col.update_card(c)
        for k in cs:
            merged_logs += col.db.scalar("select count() from revlog where cid=?", k.id) or 0
            if apply:
                col.db.execute("update revlog set cid=? where cid=?", c.id, k.id)
                k.queue = -1  # suspended
                if k.odid:  # sitting in a filtered deck: back to its own deck first
                    k.did, k.odid, k.odue = k.odid, 0, 0
                k.did = trash
                col.update_card(k)
            moved += 1
            moved_ids.append(k.id)
    col.close()
    report = {"canonical": len(canon), "problems_with_copies": len(copies), "copies_moved": moved,
              "progress_transferred": transferred, "review_logs_merged": merged_logs, "no_canonical_card": no_canon}
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if apply:
        (repo / "sources/local/lc/retired_copies.json").write_text(
            json.dumps(sorted(moved_ids), indent=0), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
