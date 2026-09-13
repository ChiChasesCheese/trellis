"""Assemble proposals/leetcode.seed.json from the small branch/map/title files.

Run from the repo root:
    PYTHONPATH=. python proposals/leetcode-build.py
"""
import glob
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
PROMPT = HERE / "leetcode.seed.prompt.md"
BRANCHES_FILE = HERE / "leetcode-branches.yaml"
MAP_GLOB = str(HERE / "leetcode-map-*.yaml")
TITLES_GLOB = str(HERE / "leetcode-titles-*.yaml")
OUT_FILE = HERE / "leetcode.seed.json"

SLUG_LINE_RE = re.compile(r"^- `([a-z0-9-]+)`", re.MULTILINE)


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def slug_to_title(slug):
    return slug.replace("-", " ")


def main():
    prompt_text = PROMPT.read_text(encoding="utf-8")
    prompt_slugs = set(SLUG_LINE_RE.findall(prompt_text))
    if not prompt_slugs:
        fail("no slugs parsed out of the prompt file")

    branches = yaml.safe_load(BRANCHES_FILE.read_text(encoding="utf-8"))
    branch_ids = [b["id"] for b in branches]
    branch_id_set = set(branch_ids)
    if len(branch_id_set) != len(branch_ids):
        fail("duplicate branch id in leetcode-branches.yaml")

    slug_to_branch = {}
    dupes = []
    for path in sorted(glob.glob(MAP_GLOB)):
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        for slug, branch in data.items():
            if slug in slug_to_branch:
                dupes.append(slug)
            slug_to_branch[slug] = branch
    if dupes:
        fail(f"slug(s) assigned more than once across map files: {sorted(set(dupes))}")

    unknown_branches = {b for b in slug_to_branch.values() if b not in branch_id_set}
    if unknown_branches:
        fail(f"map files reference branch id(s) not in leetcode-branches.yaml: {sorted(unknown_branches)}")

    mapped_slugs = set(slug_to_branch.keys())
    missing = prompt_slugs - mapped_slugs
    extra = mapped_slugs - prompt_slugs
    if missing:
        fail(f"{len(missing)} slug(s) from the prompt are not assigned to any branch: {sorted(missing)}")
    if extra:
        fail(f"{len(extra)} mapped slug(s) do not appear in the prompt: {sorted(extra)}")

    titles = {}
    for path in sorted(glob.glob(TITLES_GLOB)):
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        for slug, pair in data.items():
            if slug in titles:
                fail(f"slug {slug!r} has a title entry in more than one titles file")
            titles[slug] = pair

    unknown_title_slugs = set(titles.keys()) - prompt_slugs
    if unknown_title_slugs:
        fail(f"titles file(s) reference slug(s) not in the prompt: {sorted(unknown_title_slugs)}")

    # Group slugs by branch, preserving each branch's declared order by
    # falling back to alphabetical order of the slugs assigned to it.
    branch_children = {bid: [] for bid in branch_ids}
    for slug in sorted(mapped_slugs):
        branch_children[slug_to_branch[slug]].append(slug)

    nodes = []
    for order, branch in enumerate(branches, start=1):
        bid = branch["id"]
        children = []
        for slug in branch_children[bid]:
            pair = titles.get(slug)
            if pair:
                title, summary = pair
            else:
                title = slug_to_title(slug)
                summary = f"{slug_to_title(slug)} 相关概念。"
            children.append({
                "id": f"{bid}.{slug}",
                "title": title,
                "summary": summary,
            })
        nodes.append({
            "id": bid,
            "title": branch["title"],
            "summary": branch["summary"],
            "order": order,
            "children": children,
        })

    skeleton = {
        "domain": "leetcode",
        "title": "LeetCode",
        "lang": "zh",
        "nodes": nodes,
    }
    out = {"deck": "LeetCode", "skeleton": skeleton, "uncovered": []}

    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    leaf_count = sum(len(n["children"]) for n in nodes)
    print(f"wrote {OUT_FILE} — {len(nodes)} branches, {leaf_count} leaves")


if __name__ == "__main__":
    main()
