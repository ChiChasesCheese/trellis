"""Problems named under 同模式 that have no body yet, so the card cannot unfold them (Chi, 2026-11-15: 「990 1202 无法展开」).

    uv run python research/leetcode-unify/related_missing.py            # counts
    uv run python research/leetcode-unify/related_missing.py --write    # manifest + expand.json entries

A 同模式 item unfolds into the named problem's own statement and code, read from its body
(`trellis/build.py` load_related). This lists every such problem without a body, with its slug and Chinese title
(0x3F's title list) and the leaf it should hang on: a leaf of 0x3F's lists that has it as a candidate, preferring the
leaf of a problem that names it; else the leaf of the first problem that names it. `--write` saves the manifest to
research/leetcode-unify/related_missing.json (batches for body agents; once it exists, to
related_missing_next.json, since running agents index its rows) and adds the problems to
sources/local/lc/expand.json, so `lc_tree.py --write` puts each on its leaf once its body exists.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "vault/interviews/core/leetcode/problems"
CARDS = ROOT / "vault/interviews/core/leetcode/tree/cards"
LC = ROOT / "sources/local/lc"
OUT = Path(__file__).with_name("related_missing.json")
RELATED = re.compile(r"\*\*同模式[。：:]?\*\*[：:]?(.*)")


def main() -> int:
    titles = json.loads((LC / "0x3f/lc_titles.json").read_text(encoding="utf-8"))
    have = {}
    for f in P.glob("*.md"):
        m = re.search(r"^\*\*LC (\d+) ", f.read_text(encoding="utf-8"), re.M)
        if m:
            have[int(m.group(1))] = f.stem
    leaf_of = {}  # slug -> its tree leaf
    for f in CARDS.rglob("lct-*.md"):
        node = re.search(r"^node: (\S+)", f.read_text(encoding="utf-8")[:400], re.M)
        if node and not f.name.startswith("lct-learn-"):
            leaf_of[f.stem[4:]] = node.group(1)
    tree = json.loads((LC / "tree.json").read_text(encoding="utf-8"))
    cand: dict[int, list[str]] = {}  # number -> leaves listing it

    def walk(n: dict) -> None:
        for c in n.get("candidates", []):
            cand.setdefault(c["num"], []).append(n["id"])
        for k in n.get("children", []):
            walk(k)
    for lst in tree["lists"]:
        walk(lst)
    refs: dict[int, list[str]] = {}
    for f in sorted(P.glob("*.md")):
        m = RELATED.search(f.read_text(encoding="utf-8"))
        for n in dict.fromkeys(int(x) for x in re.findall(r"LC (\d+)", m.group(1) if m else "")):
            if n not in have:
                refs.setdefault(n, []).append(f.stem)
    rows = []
    for n, who in sorted(refs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        t = titles.get(str(n))
        if not t:
            print(f"  ! LC {n}: not in the title list, skipped (named by {who[0]})")
            continue
        homes = [leaf_of[w] for w in who if w in leaf_of]
        options = cand.get(n, [])
        leaf = next((h for h in homes if h in options), options[0] if options else (homes[0] if homes else None))
        rows.append({"num": n, "slug": t["slug"], "title": t["zh"], "en": t["en"], "leaf": leaf, "named_by": who})
    print(f"{len(rows)} problems; {sum(1 for r in rows if not r['leaf'])} without a leaf")
    if "--write" not in sys.argv:
        return 0
    out = OUT if not OUT.exists() else OUT.with_name("related_missing_next.json")  # agents index rows of the first one
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    exp = json.loads((LC / "expand.json").read_text(encoding="utf-8"))
    listed = {c["slug"] for v in exp.values() for c in v}
    added = 0
    for r in rows:
        if r["leaf"] and r["slug"] not in listed:
            exp.setdefault(r["leaf"], []).append({"num": r["num"], "title": r["title"], "slug": r["slug"],
                                                  "rating": 0, "members": False, "importance": 0.0})
            added += 1
    (LC / "expand.json").write_text(json.dumps(exp, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out.name}; {added} added to expand.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
