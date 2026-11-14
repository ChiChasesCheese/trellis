"""After the migration: delete the old LeetCode copies and archive, and turn LeetCode Tops into Under the Hood (Chi, 2026-11-14).

    uv run --no-project --with anki==26.9.3 python -I research/leetcode-unify/restructure.py <collection.anki2> <repo> [--apply]

Run with desktop Anki closed and a backup taken. Chi: 「lead code 其他的可以删了，就是把模式卡 under the hood 这种比较有意思的
留下来……LeetCodeTops 直接改名……Under the Hood，以后就包含所有 LeetCode 或者说算法与数据结构相关的非题目直接的一些模式东西」.
- deletes every note in `📦 其他::待删除 · 旧 LeetCode 副本`, in the archive `LeetCode Tops::99 …`, and the two
  problem-intuition cards left in deck 24 (a problem has one card);
- renames LeetCode Tops to Under the Hood, with 01 工具里的数据结构与算法, 02 解题模式与 Python 技巧（TikTok）,
  03 Amazon 解题模式 (decks 19 and 20 merged); empty sub-decks go;
- rewrites the home records of sprint and daily decks (sources/local/plan/*homes.json) to the new names.
Without --apply it prints what it would do.
"""
import json
import sys
from pathlib import Path

from anki.collection import Collection

OLD, NEW = "LeetCode Tops", "Under the Hood"
TRASH = "📦 其他::待删除 · 旧 LeetCode 副本"
RENAME = {  # old sub-deck prefix -> new sub-deck
    "26 ": "01 工具里的数据结构与算法（under the hood）",
    "24 ": "02 解题模式与 Python 技巧（TikTok）",
    "20 ": "03 Amazon 解题模式",
    "19 ": "03 Amazon 解题模式",
}
LEFTOVER_IDS = ("tlc-find-minimum-in-rotated-sorted-array-0-intuition-left",
                "tlc-find-minimum-in-rotated-sorted-array-0-intuition-right")


def new_name(name: str) -> str | None:
    """The new deck name for an old LeetCode Tops deck, or None when the deck is not kept."""
    if name == OLD:
        return NEW
    if not name.startswith(OLD + "::"):
        return name
    parts = name.split("::")
    top = next((v for k, v in RENAME.items() if parts[1].startswith(k)), None)
    return "::".join([NEW, top] + parts[2:]) if top else None


def main() -> int:
    col_path, repo = sys.argv[1], Path(sys.argv[2])
    apply = "--apply" in sys.argv
    col = Collection(col_path)
    doomed = set(col.find_notes(f'"deck:{TRASH}"')) | set(col.find_notes(f'"deck:{OLD}::99*"'))
    doomed |= set(col.find_notes(" OR ".join(f'"tag:id::{i}"' for i in LEFTOVER_IDS)))
    print(f"delete {len(doomed)} notes")
    moves: dict[str, list[int]] = {}
    for d in col.decks.all_names_and_ids():
        if d.name == OLD or d.name.startswith(OLD + "::"):
            target = new_name(d.name)
            cids = [c for c in col.find_cards(f'did:{d.id}') if col.get_card(c).nid not in doomed]
            if cids:
                if target is None:
                    print(f"  ! {len(cids)} cards left in {d.name}: no new home; kept under {NEW}::99 其他")
                    target = f"{NEW}::99 其他"
                moves.setdefault(target, []).extend(cids)
    for t, cids in sorted(moves.items()):
        print(f"  {len(cids):5} -> {t}")
    if not apply:
        col.close()
        return 0
    col.remove_notes(list(doomed))
    for target, cids in moves.items():
        did = col.decks.id(target)
        col.set_deck(cids, did)
    old_conf = col.decks.config_dict_for_deck_id(col.decks.id_for_name(OLD)) if col.decks.id_for_name(OLD) else None
    for d in sorted(col.decks.all_names_and_ids(), key=lambda d: -len(d.name)):  # children first
        if (d.name == OLD or d.name.startswith(OLD + "::") or d.name == TRASH) and not col.find_cards(f"did:{d.id}"):
            col.decks.remove([d.id])
    if old_conf:  # Under the Hood keeps the preset LeetCode Tops had
        for d in col.decks.all_names_and_ids():
            if d.name == NEW or d.name.startswith(NEW + "::"):
                deck = col.decks.get(d.id)
                deck["conf"] = old_conf["id"]
                col.decks.save(deck)
    col.close()
    for f in (repo / "sources/local/plan").glob("*homes.json"):
        h = json.loads(f.read_text(encoding="utf-8"))
        changed = {k: (new_name(v) or f"{NEW}::99 其他") for k, v in h.items()}
        f.write_text(json.dumps(changed, ensure_ascii=False, indent=0), encoding="utf-8")
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
