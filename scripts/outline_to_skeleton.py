"""Turn a reviewed domain outline (research/domains/<d>/outline.md) into skeleton/<d>.yaml plus a sidecar of leaf notes.

    uv run python scripts/outline_to_skeleton.py k8s --title "Kubernetes：从零到 2026 实践" --deck "Kubernetes"

Outline grammar (the one the 2026-11 survey agents wrote):
- `# 第 N 部分 …` lines (optional) open a part; `## …` lines open a theme/chapter under it (or at the top when the
  outline has no parts). Everything from `## 不收` on is ignored.
- `- * Title — summary 〔出处：…〕` is a core leaf; without `* ` it is a later-wave leaf. `(需先: <leaf title>)` becomes
  a `requires` edge. Chapter lines starting `图：` or `2026：` are kept as notes for the writers.

Ids are stable slugs: parts `p1…`, themes `<part>.t01…`, leaves `<theme>.<english-slug>`. The citation and the
chapter notes go to research/domains/<d>/leaves.yaml (the skeleton has no field for them); card writers read both.
Re-running overwrites both files, so edit the outline, not the outputs.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CITE = re.compile(r"\s*〔(?:出处：)?(.*?)〕\s*$")
NEED = re.compile(r"\s*[（(]需先[:：]\s*(.*?)[）)]")


def slug(title: str, taken: set[str]) -> str:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+]*", title)
    base = "-".join(w.lower() for w in words)[:48].strip("-") or "leaf"
    if base == "leaf":
        print(f"warning: no English word in {title!r}: its id falls back to 'leaf'; add the English term to the title", file=sys.stderr)
    s, n = base, 2
    while s in taken:
        s, n = f"{base}-{n}", n + 1
    taken.add(s)
    return s


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse(outline: str) -> tuple[list[dict], dict]:
    parts: list[dict] = []
    meta: dict = {}
    part = theme = None
    has_parts = bool(re.search(r"^# 第 \d+ 部分", outline, re.M))
    titles: dict[str, str] = {}
    pending_req: list[tuple[dict, str]] = []
    for line in outline.splitlines():
        if line.startswith("## 不收"):
            break
        if has_parts and line.startswith("# 第"):
            part = {"id": f"p{len(parts) + 1}", "title": clean(line[2:]), "children": []}
            parts.append(part)
            theme = None
            continue
        if line.startswith("## "):
            holder = part["children"] if has_parts and part else parts
            prefix = f"{part['id']}." if has_parts and part else ""
            theme = {"id": f"{prefix}t{len(holder) + 1:02d}", "title": clean(re.sub(r"^[一二三四五六七八九十\d]+[、.]\s*", "", line[3:])),
                     "children": []}
            holder.append(theme)
            continue
        if theme is not None and re.match(r"^(图|2026)：", line):
            meta.setdefault(theme["id"], {}).setdefault("notes", []).append(clean(line))
            continue
        m = re.match(r"^- (\* )?(.*)$", line)
        if not (m and theme is not None):
            continue
        core, body = bool(m.group(1)), m.group(2)
        cite = CITE.search(body)
        body = CITE.sub("", body) if cite else body
        reqs = NEED.findall(body)
        body = NEED.sub("", body)
        title, _, summary = body.partition(" — ")
        leaf = {"id": "", "title": clean(title), "summary": clean(summary) or clean(title), "core": core}
        theme["children"].append(leaf)
        meta_entry = {"cite": clean(cite.group(1)) if cite else ""}
        leaf["_meta"] = meta_entry
        for r in reqs:
            pending_req.append((leaf, clean(r)))
    taken: set[str] = set()
    for top in parts:
        for th in (top["children"] if has_parts else [top]):
            for leaf in th["children"]:
                leaf["id"] = f"{th['id']}.{slug(leaf['title'], taken)}"
                titles[leaf["title"].lower()] = leaf["id"]
                meta[leaf["id"]] = leaf.pop("_meta")
    for leaf, req in pending_req:
        target = titles.get(req.lower()) or next((i for t, i in titles.items() if req.lower() in t), None)
        if target:
            leaf.setdefault("requires", []).append(target)
        else:
            print(f"warning: {leaf['id']}: prerequisite not found: {req}", file=sys.stderr)
    for top in parts:  # drop empty themes, give parts/themes a summary
        top["summary"] = top.get("summary") or top["title"]
        for th in top["children"]:
            th.setdefault("summary", th["title"])
    for i, top in enumerate(parts, 1):
        top["order"] = i
    return parts, meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("--title", required=True)
    ap.add_argument("--deck", required=True)
    ap.add_argument("--order", default="core-first", choices=["core-first", "skeleton"])
    ap.add_argument("--new-per-day", type=int, default=20)
    args = ap.parse_args()
    outline = (ROOT / f"research/domains/{args.domain}/outline.md").read_text(encoding="utf-8")
    nodes, meta = parse(outline)
    head = (f"# Generated from research/domains/{args.domain}/outline.md by scripts/outline_to_skeleton.py:\n"
            f"# edit the outline, not this file. Citations and chapter notes: research/domains/{args.domain}/leaves.yaml.\n")
    doc = {"domain": args.domain, "title": args.title, "deck": args.deck, "lang": "zh",
           "vault": f"domains/{args.domain}", "deck_depth": 1,
           "study": {"order": args.order, "mix": "new-first", "new_per_day": args.new_per_day, "reviews_per_day": 200},
           "nodes": nodes}
    out = ROOT / f"skeleton/{args.domain}.yaml"
    out.write_text(head + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    side = ROOT / f"research/domains/{args.domain}/leaves.yaml"
    side.write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    leaves = [m for k, m in meta.items() if "cite" in m]
    print(f"{out}: {len(nodes)} top nodes, {len(leaves)} leaves; sidecar {side}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
