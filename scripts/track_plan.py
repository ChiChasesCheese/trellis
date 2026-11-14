"""A role track: the knowledge one kind of interview needs, as an ordered list of skeleton leaves from any domain.

    uv run python scripts/track_plan.py tracks/ai-infra-sdet.yaml            # print the parts
    uv run python scripts/track_plan.py <overlay.yaml> -o <plan.json>        # a company overlay on a track -> plan

Chi (2026-11-13): prepare for a kind of role (AI-infrastructure SDET, inference infrastructure, inference deployment),
with a company as a thin layer on top, so the same deck can be renamed and reorganised for the next role. The cards stay
in their domains; scripts/company_deck.py deals a plan into a sprint deck.

A track file (tracks/<name>.yaml, public):

    track: ai-infra-sdet
    title: …
    sections:
    - title: AI 从零开始
      parts:
      - node: llm-inference:basics            # a node: each leaf under it is a part (its own cards, by step)
      - node: test-release:strategy.integration
        also: [card-id, …]                    # older cards on the same point: a follow-on part "… · 延伸"
      - label: pytest 夹具（fixture）          # a free part: the cards of some nodes, then some cards
        nodes: [python:engineering.testing]
        cards: [card-id, …]

A sibling track can reuse one: `base: tracks/ai-infra-sdet.yaml` plus `order: [section titles]`.

An overlay file (private, next to the company's research) adds `track: <path>`, `deck: "6 <Company>"`, its own
`before:` / `after:` sections in the same format, and `extend: {<section title>: [parts]}` for parts appended to a
track section (cards from private domains go here, never into a public track). Numbers come from the order.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def skeletons() -> dict[str, dict]:
    out = {}
    for f in (ROOT / "skeleton").glob("*.yaml"):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if isinstance(d, dict) and d.get("domain"):
            out[d["domain"]] = d
    return out


def leaves(nodes: list[dict]) -> list[dict]:
    out = []
    for n in nodes:
        kids = n.get("children") or []
        out += leaves(kids) if kids else [n]
    return out


def find(nodes: list[dict], nid: str) -> dict | None:
    for n in nodes:
        if n["id"] == nid:
            return n
        hit = find(n.get("children") or [], nid)
        if hit:
            return hit
    return None


def card_index(sk: dict[str, dict]) -> dict[tuple[str, str], list[str]]:
    """(domain, node) -> card ids in step order."""
    by_node = defaultdict(list)
    for dom, d in sk.items():
        base = ROOT / "vault" / d["vault"] if d.get("vault") else None
        if not base or not base.exists():
            continue
        for f in base.rglob("*.md"):
            head = f.read_text(encoding="utf-8", errors="ignore")[:600]
            m, n = re.search(r"^id: (\S+)", head, re.M), re.search(r"^node: (\S+)", head, re.M)
            if head.startswith("---") and m and n:
                st = re.search(r"^step: (\d+)", head, re.M)
                by_node[(dom, n.group(1))].append((int(st.group(1)) if st else 999, f.name, m.group(1)))
    return {k: [i for _, _, i in sorted(v)] for k, v in by_node.items()}


def short(title: str) -> str:
    return re.split(r"[：（]", title)[0][:30]


def expand(sections: list[dict], sk: dict, by_node: dict) -> list[dict]:
    """[{title, parts: [{name, ids}]}] with every node resolved to its cards."""
    out = []
    for sec in sections:
        parts = []
        for p in sec.get("parts", []):
            if "node" in p:
                dom, nid = p["node"].split(":", 1)
                node = find(sk[dom]["nodes"], nid)
                if node is None:
                    raise SystemExit(f"unknown node {p['node']}")
                for leaf in leaves([node]):
                    parts.append({"name": p.get("label") or short(leaf["title"]), "ids": by_node.get((dom, leaf["id"]), [])})
                if p.get("also"):
                    parts.append({"name": (p.get("label") or short(node["title"])) + " · 延伸", "ids": p["also"]})
            else:
                ids = [c for ref in p.get("nodes", []) for c in by_node.get(tuple(ref.split(":", 1)), [])]
                parts.append({"name": p["label"], "ids": ids + list(p.get("cards", []))})
        out.append({"title": sec["title"], "parts": parts})
    return out


def load_track(path: Path) -> dict:
    """A track; one with `base:` and `order:` reuses another track's sections, reordered and filtered by title."""
    t = yaml.safe_load(path.read_text(encoding="utf-8"))
    if t.get("base"):
        base = {s["title"]: s for s in load_track(ROOT / t["base"])["sections"]}
        t["sections"] = [base[x] for x in t["order"]] + t.get("sections", [])
    return t


def plan(spec: Path) -> tuple[list[dict], dict]:
    d = yaml.safe_load(spec.read_text(encoding="utf-8"))
    is_track = "sections" in d or "base" in d  # a track names itself in `track:`; an overlay points at one
    track = load_track(spec) if is_track else load_track(ROOT / d["track"])
    d = {} if is_track else d
    extend = d.get("extend") or {}
    sections = d.get("before", []) + [{**sec, "parts": sec["parts"] + extend.get(sec["title"], [])} for sec in track["sections"]] \
        + d.get("after", [])
    sk = skeletons()
    used, out = set(), []
    for s, sec in enumerate(expand(sections, sk, card_index(sk)), 1):
        n = 0
        for p in sec["parts"]:
            fresh = [c for c in dict.fromkeys(p["ids"]) if c not in used]
            used.update(fresh)
            if fresh:
                n += 1
                out.append({"label": f"{s:02d} {sec['title']}::{n:02d} {p['name']}", "ids": fresh})
    return out, d


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    parts, d = plan(Path(args[0]))
    if "-o" in args:
        out = Path(args[args.index("-o") + 1])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(parts, ensure_ascii=False, indent=1), encoding="utf-8")
    secs = defaultdict(int)
    for p in parts:
        secs[p["label"].split("::")[0]] += len(p["ids"])
    print(f"{len(parts)} parts, {sum(secs.values())} cards")
    for k, v in secs.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
