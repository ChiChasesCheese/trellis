"""tree.txt -> skeleton/psych.yaml and one anchor list per card group (research/domains/psych/anchors-<G>.md).

    python3 research/domains/psych/gen_tree.py            # write both, print the counts
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

HEADER = """# People as they are measured: the findings from psychology, behavioural economics and sociology that hold up when
# the studies are repeated, chosen for how much they change everyday judgment, self-management, learning, relationships,
# career and life decisions. Generated from research/domains/psych/tree.txt by gen_tree.py: edit that file, not this one.
# Depth is fixed: field -> theme -> concept. A leaf is one concept. `core: true` marks the first 200 (the first wave of
# cards); the other leaves wait for a later wave. Evidence grades and source studies are in the tree file.
domain: psych
title: 人性与决策：经得起重做的心理学、行为经济学与社会学
deck: "9 人性与决策"
lang: zh
vault: domains/psych
deck_depth: 1
study:
  order: core-first
  mix: new-first
  new_per_day: 20
  reviews_per_day: 200
nodes:
"""

# which card group owns which level-1 or level-2 node (longest prefix wins)
GROUPS = {
    "evidence.method": "A", "judge": "A",
    "self": "B",
    "evidence.myth": "C", "learn": "C", "career": "C",
    "social": "D", "life": "D",
    "group": "E", "game": "E",
    "persona.mbti": "F", "persona.jung": "F", "persona.use": "F",  # added 2026-11-19 at Chi's request
    "persona.big5": "G",
}


def group_of(leaf_id: str) -> str:
    best = max((k for k in GROUPS if leaf_id == k or leaf_id.startswith(k + ".")), key=len)
    return GROUPS[best]


def parse() -> list[dict]:
    tops: list[dict] = []
    for n, line in enumerate((HERE / "tree.txt").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        mark, _, rest = line.partition(" ")
        if mark not in {"#", "##", "*", "-"} or "|" not in rest or rest.startswith(" "):
            continue  # a comment line
        parts = [p.strip() for p in rest.split(" | ")]
        if mark == "#":
            tops.append({"id": parts[0], "title": parts[1], "summary": parts[2], "children": []})
        elif mark == "##":
            tops[-1]["children"].append({"id": parts[0], "title": parts[1], "summary": parts[2], "children": []})
        else:
            if len(parts) < 5:
                raise SystemExit(f"tree.txt:{n}: a leaf needs slug | title | summary | grade | anchor")
            parent = tops[-1]["children"][-1]
            leaf = {"id": f"{parent['id']}.{parts[0]}", "title": parts[1], "summary": parts[2], "grade": parts[3],
                    "anchor": parts[4], "core": mark == "*", "requires": [], "tags": []}
            for extra in parts[5:]:
                key, _, value = extra.partition("=")
                if key == "req":
                    leaf["requires"] = [v.strip() for v in value.split(",")]
                elif key == "tag":
                    leaf["tags"] = [v.strip() for v in value.split(",")]
                else:
                    raise SystemExit(f"tree.txt:{n}: unknown field {extra!r}")
            if leaf["grade"] not in {"A", "B", "C"}:
                raise SystemExit(f"tree.txt:{n}: grade must be A, B or C")
            parent["children"].append(leaf)
    return tops


def q(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)  # a JSON string is a valid YAML double-quoted scalar


def skeleton(tops: list[dict]) -> str:
    out = [HEADER]
    for i, top in enumerate(tops, 1):
        out.append(f"- id: {top['id']}\n  order: {i}\n  title: {q(top['title'])}\n  summary: {q(top['summary'])}\n  children:\n")
        for mid in top["children"]:
            out.append(f"  - id: {mid['id']}\n    title: {q(mid['title'])}\n    summary: {q(mid['summary'])}\n    children:\n")
            for leaf in mid["children"]:
                out.append(f"    - id: {leaf['id']}\n")
                if leaf["core"]:
                    out.append("      core: true\n")
                out.append(f"      title: {q(leaf['title'])}\n      summary: {q(leaf['summary'])}\n")
                if leaf["requires"]:
                    out.append(f"      requires: [{', '.join(leaf['requires'])}]\n")
    return "".join(out)


def card_id(leaf_id: str) -> str:
    top, _, slug = leaf_id.split(".", 2)  # the theme is not part of the card id: slugs are unique inside a field
    return f"psy-{top}-{slug}"


def main() -> None:
    tops = parse()
    leaves = [leaf for top in tops for mid in top["children"] for leaf in mid["children"]]
    ids = Counter(card_id(leaf["id"]) for leaf in leaves)
    dup = [k for k, v in ids.items() if v > 1]
    if dup:
        raise SystemExit(f"duplicate card ids: {dup}")
    (ROOT / "skeleton/psych.yaml").write_text(skeleton(tops), encoding="utf-8")

    grade_word = {"A": "强", "B": "中", "C": "弱"}
    by_group: dict[str, list[str]] = {}
    for leaf in leaves:
        if not leaf["core"]:
            continue
        top = leaf["id"].split(".")[0]
        tags = f" · tags: [{', '.join(leaf['tags'])}]" if leaf["tags"] else ""
        by_group.setdefault(group_of(leaf["id"]), []).append(
            f"### {leaf['title']}\n\n"
            f"- node: `{leaf['id']}` · file: `vault/domains/psych/cards/{top}/{card_id(leaf['id'])}.md`{tags}\n"
            f"- 一句话：{leaf['summary']}\n"
            f"- 证据等级：{leaf['grade']}（卡片上写「证据 · {grade_word[leaf['grade']]}」）\n"
            f"- anchor: {leaf['anchor']}\n")
    for g, rows in sorted(by_group.items()):
        (HERE / f"anchors-{g}.md").write_text(
            f"# Group {g}: {len(rows)} cards\n\nOne card per entry, in this order. The anchor is a starting point from "
            f"memory: check every number against the paper or a reliable summary before it goes on a card.\n\n"
            + "\n".join(rows), encoding="utf-8")

    # The whole map as an Obsidian outline (Mindmap NextGen): every concept, carded or not. No frontmatter (the plugin's
    # YAML parser breaks on mobile). scripts/knowledge_tree.py draws the other note, which shows only what has cards.
    cards = {f.stem for f in (ROOT / "vault/domains/psych/cards").glob("*/*.md")}
    lines = ["# 人性与决策 概念全图", ""]
    for top in tops:
        mine = [leaf for mid in top["children"] for leaf in mid["children"]]
        lines.append(f"- {top['title']} · {len(mine)}")
        for mid in top["children"]:
            lines.append(f"  - {mid['title']} · {len(mid['children'])} <!-- markmap: fold -->")
            for leaf in mid["children"]:
                todo = "" if card_id(leaf["id"]) in cards else " · 待写"
                lines.append(f"    - {leaf['title']} · 证据{grade_word[leaf['grade']]}{todo}")
    (ROOT / "vault/domains/psych/人性与决策 概念全图.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    core = [leaf for leaf in leaves if leaf["core"]]
    print(f"{len(tops)} fields, {sum(len(t['children']) for t in tops)} themes, {len(leaves)} leaves, {len(core)} core")
    for top in tops:
        mine = [leaf for mid in top["children"] for leaf in mid["children"]]
        print(f"  {top['id']:9} {sum(leaf['core'] for leaf in mine):3} core / {len(mine):3} leaves")
    print("groups:", {g: len(rows) for g, rows in sorted(by_group.items())})
    print("grades (core):", dict(Counter(leaf["grade"] for leaf in core)))


if __name__ == "__main__":
    main()
