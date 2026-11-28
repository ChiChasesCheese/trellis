"""Export: the Atlas data contract, written from tracked skeletons, tracked cards and the Snapshots.

The Atlas site and agents read `atlas-data/` and nothing else. The output is a pure function of the commit: no wall
clock, no machine paths (`generated_at` is the commit's date, or the Snapshot's date outside git).
"""

from __future__ import annotations

import json
import re
import shutil
from importlib import resources
from pathlib import Path

from .atlas import PublishedDomain
from .snapshot import level, load_snapshots

REACH_DEFINITION = ("学过（Reach）：一个节点下被学过至少一次的卡片占全部卡片的比例；"
                    "卡片自己复习过，或者以它为答案的测试题复习过，都算学过。")
SUMMARY = ("Trellis is a skeleton-constrained knowledge base: one mind map per subject, and every study card hangs "
           "off a node of that map. Reach is the share of a node's cards that have been studied at least once "
           "(a card counts once it, or the test question built on it, has been reviewed); Hold measures whether "
           "what was studied is retained. This site publishes the maps, the cards and a dated Snapshot of Reach and Hold per node.")
SCHEMA_KINDS = ("index", "domain", "card", "snapshot", "history", "daily")

_EMBED = re.compile(r"!\[\[[^\]]*\]\]")
_WIKI_ALIAS = re.compile(r"\[\[[^\]|]*\|([^\]]*)\]\]")
_WIKI = re.compile(r"\[\[([^\]]*)\]\]")
_OBS_LINK = re.compile(r"\[([^\]]*)\]\(obsidian://[^)]*\)")
_OBS_BARE = re.compile(r"<?obsidian://[^\s)>]*>?")


def plain_markdown(text: str) -> str:
    """Obsidian links out, everything else (mermaid fences, HTML) kept: `[[x|y]]` -> `y`, `[[x]]` -> `x`."""
    text = _EMBED.sub("", text)
    text = _WIKI_ALIAS.sub(r"\1", text)
    text = _WIKI.sub(r"\1", text)
    text = _OBS_LINK.sub(r"\1", text)
    return _OBS_BARE.sub("", text)


def schema_text(kind: str) -> str:
    return (resources.files("trellis") / "atlas_schema" / f"{kind}.schema.json").read_text(encoding="utf-8")


def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _round(x):
    return None if x is None else round(x, 3)


def export(published: dict[str, PublishedDomain], snapshots: list[dict], out: str | Path,
           generated_at: str = "") -> dict:
    """Write the contract into `out` (emptied first). Returns {file kind: count} for the caller to print."""
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    latest = snapshots[-1] if snapshots else None
    snap_date = latest["date"] if latest else None

    index_rows = []
    counts = {"domains": 0, "nodes": 0, "cards": 0}
    for domain, pub in published.items():
        sk = pub.skeleton
        snap = (latest or {}).get("domains", {}).get(domain)
        snap_nodes = (snap or {}).get("nodes", {})
        subtree: dict[str, int] = {}
        for card in pub.cards:
            for n in sk.by_id[card.node].path():
                subtree[n.id] = subtree.get(n.id, 0) + 1
        readings: dict[str, list[dict]] = {}
        for r in pub.readings:
            row = {"title": r.title, **({"url": r.url} if r.url else {})}
            for nid in r.nodes:
                readings.setdefault(nid, []).append(row)

        nodes = []
        walk = [n for n in sk.walk() if n.id in pub.nodes]
        for order, node in enumerate(walk):
            cards = subtree.get(node.id, 0)
            entry = snap_nodes.get(node.id, {})
            studied = reach = lvl = hold = None
            flags: list[str] = []
            if snap is not None:
                studied = min(entry.get("studied", 0), cards)
                reach = round(studied / cards, 3) if cards else None
                hold = entry.get("hold")
                flags = list(entry.get("flags", []))
            lvl = level(studied, cards)
            nodes.append({
                "id": node.id, "parent": node.parent.id if node.parent else None, "title": node.title,
                "summary": node.summary, "core": node.core,
                "requires": [r for r in node.requires if r in pub.nodes],
                "depth": len(node.path()) - 1, "order": order, "leaf": node.is_leaf,
                "cards": cards, "studied": studied, "reach": reach, "level": lvl, "hold": hold,
                "flags": flags, "readings": readings.get(node.id, []),
            })
        leaves = [n for n in nodes if n["leaf"]]
        weak = [n["id"] for n in leaves if "weak" in n["flags"]]
        uncovered = [n["id"] for n in leaves if n["cards"] == 0]
        total = len(pub.cards)
        done = None if snap is None else min((snap or {}).get("studied", 0), total)
        row = {"id": domain, "title": sk.title, "lang": sk.lang, "nodes": len(nodes), "leaves": len(leaves),
               "cards": total, "studied": done,
               "reach": round(done / total, 3) if done is not None and total else None,
               "level": level(done, total), "hold": (snap or {}).get("hold"),
               "weak": weak, "uncovered": uncovered}
        index_rows.append(row)
        _write(out / "d" / f"{domain}.json", {"schema": "trellis.domain/1", **{**row, "nodes": nodes},
                                              "snapshot_date": snap_date})
        _write_md(out / "d" / f"{domain}.md", row, nodes)
        _write_cards(out / "d" / domain / "cards.jsonl", pub)
        counts["domains"] += 1
        counts["nodes"] += len(nodes)
        counts["cards"] += total

    history: dict[str, list[dict]] = {d: [] for d in published}
    for s in snapshots:
        for d, block in s["domains"].items():
            if d in history:
                history[d].append({"date": s["date"], **{k: block[k] for k in ("cards", "studied", "hold") if k in block}})
    _write(out / "index.json", {"schema": "trellis.index/1", "generated_at": generated_at or snap_date or "",
                                "snapshot_date": snap_date, "reach_definition": REACH_DEFINITION,
                                "domains": index_rows})
    _write(out / "history.json", {"schema": "trellis.history/1", "domains": history})
    _write(out / "daily.json", {"schema": "trellis.daily/1", "date": snap_date,
                                "daily": (latest or {}).get("daily", {})})
    for kind in SCHEMA_KINDS:
        (out / "schema").mkdir(exist_ok=True)
        (out / "schema" / f"{kind}.schema.json").write_text(schema_text(kind), encoding="utf-8")
    (out / "llms.txt").write_text(_llms(index_rows), encoding="utf-8")
    return counts


def _write_md(path: Path, row: dict, nodes: list[dict]) -> None:
    lines = [f"# {row['title']} (`{row['id']}`)", "",
             f"{row['cards']} cards, {row['leaves']} leaves"
             + (f", {row['studied']} studied" if row["studied"] is not None else "") + ". "
             "Each line: title `id` studied/cards, then flags.", ""]
    for n in nodes:
        studied = "?" if n["studied"] is None else n["studied"]
        flags = f" [{', '.join(n['flags'])}]" if n["flags"] else ""
        lines.append(f"{'  ' * n['depth']}- {n['title']} `{n['id']}` {studied}/{n['cards']}{flags}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_cards(path: Path, pub: PublishedDomain) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    show = pub.skeleton.show or ""
    with path.open("w", encoding="utf-8") as fh:
        for card in pub.cards:
            q, a = card.render(show)
            line = {"schema": "trellis.card/1", "id": card.id, "node": card.node, "type": card.type,
                    "step": card.step, "q": plain_markdown(q), "a": plain_markdown(a), "tags": card.tags}
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")


def _llms(rows: list[dict]) -> str:
    lines = ["# Trellis Atlas", "", f"> {SUMMARY}", "", "## Data", "",
             "- [index.json](index.json): every domain, its Reach and Hold",
             "- [history.json](history.json): Reach and Hold per domain over the dated Snapshots",
             "- [daily.json](daily.json): cards reviewed per day", "",
             "## Domains", ""]
    for r in rows:
        lines.append(f"- [{r['title']}](d/{r['id']}.md): outline with studied/cards per node; "
                     f"[cards](d/{r['id']}/cards.jsonl) ({r['cards']}); [tree](d/{r['id']}.json)")
    lines += ["", "## Schemas", ""] + [f"- [{k}](schema/{k}.schema.json)" for k in SCHEMA_KINDS]
    return "\n".join(lines) + "\n"
