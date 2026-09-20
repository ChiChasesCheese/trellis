"""Acceptance gate for the design-problem bank in system-design (BUILD.md).

    uv run python scripts/check_design_problems.py problems.social.news-feed [...]
    uv run python scripts/check_design_problems.py --all

A problem leaf is done when it has: a solution article written in the vault
(deep enough, every required section, a diagram, sources), a drill whose
grading points link to real cards and to the solution, at least six cards
with translations and steps, and at least two source readings — with every
commercial prep site linked but marked `no-archive`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from trellis.project import load_project  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "problems"
MIN_SOLUTION_CHARS = 9000
MIN_CARDS = 6
MIN_DEEP_DIVES = 4
SECTIONS = ["题目与范围", "需求", "容量估算", "核心实体与 API", "高层设计", "深入探讨",
            "瓶颈、故障与演进", "面试官会追问什么", "常见错误", "五分钟讲法", "来源与延伸"]
# Sites whose worked answers are their product. Link, never copy.
COMMERCIAL = ("hellointerview.com", "bytebytego.com", "designgurus.io", "educative.io",
              "tryexponent.com", "interviewing.io", "systemdesignschool.io", "codemia.io",
              "leetcode.com", "algomaster.io", "systemdesign.one", "amazon.com", "oreilly.com")
# Repositories that republish a paid course or book: never a source.
MIRRORS = ("Jeevan-kumar-Raj/Grokking-System-Design", "liquidslr/system-design-notes")
WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def check(project, leaf_id: str) -> list[str]:
    problems: list[str] = []
    card_ids = {c.id for c in project.cards}
    cards = [c for c in project.cards if c.node == leaf_id and not c.adopted]
    readings = [r for r in project.readings if leaf_id in r.nodes]
    drills = [d for d in project.drills if leaf_id in d.nodes]

    solutions = [r for r in readings if r.authored]
    if len(solutions) != 1:
        problems.append(f"expected exactly one authored solution reading, found {len(solutions)}")
    for s in solutions:
        text = s.path.read_text(encoding="utf-8")
        if s.prose < MIN_SOLUTION_CHARS:
            problems.append(f"{s.path.name}: {s.prose} chars, need ≥ {MIN_SOLUTION_CHARS}")
        heads = re.findall(r"^## (.+)$", text, re.MULTILINE)
        missing = [h for h in SECTIONS if not any(x.strip().startswith(h) for x in heads)]
        if missing:
            problems.append(f"{s.path.name}: missing sections {missing}")
        deep = text.split("## 深入探讨", 1)[1].split("\n## ", 1)[0] if "## 深入探讨" in text else ""
        if len(re.findall(r"^### ", deep, re.MULTILINE)) < MIN_DEEP_DIVES:
            problems.append(f"{s.path.name}: fewer than {MIN_DEEP_DIVES} deep dives (### under 深入探讨)")
        if "```mermaid" not in text:
            problems.append(f"{s.path.name}: no mermaid diagram")
        if any(m.lower() in text.lower() for m in MIRRORS):
            problems.append(f"{s.path.name}: links a mirror of paid material")
        tail = text.split("## 来源与延伸", 1)[1] if "## 来源与延伸" in text else ""
        if len(re.findall(r"https?://", tail)) < 3:
            problems.append(f"{s.path.name}: fewer than 3 source links under 来源与延伸")

    if len(cards) < MIN_CARDS:
        problems.append(f"{len(cards)} card(s), need ≥ {MIN_CARDS}")
    for c in cards:
        if project.skeleton.lang == "en" and not c.tr.get("zh"):
            problems.append(f"card {c.id}: no zh translation")
        if c.step is None:
            problems.append(f"card {c.id}: no step")

    if not drills:
        problems.append("no drill attached to this leaf")
    for d in drills:
        text = d.path.read_text(encoding="utf-8")
        points = text.split("Grading points", 1)[1] if "Grading points" in text else ""
        linked = [w.strip() for w in WIKILINK.findall(points)]
        real = [w for w in linked if w in card_ids]
        if len(real) < 4:
            problems.append(f"{d.path.name}: {len(real)} grading-point link(s) to real cards, need ≥ 4")
        dead = [w for w in linked if w not in card_ids and not any(w == s.path.stem for s in solutions)]
        if dead:
            problems.append(f"{d.path.name}: links to nothing: {dead[:4]}")
        if solutions and solutions[0].path.stem not in text:
            problems.append(f"{d.path.name}: does not link its solution [[{solutions[0].path.stem}]]")

    pointers = [r for r in readings if r.url]
    if len(pointers) < 2:
        problems.append(f"{len(pointers)} source reading(s) with a url, need ≥ 2")
    for r in pointers:
        if any(m.lower() in r.url.lower() for m in MIRRORS):
            problems.append(f"{r.path.name}: points at a mirror of paid material — cite the original instead")
        host = urlsplit(r.url).netloc.lower()
        if any(host == h or host.endswith("." + h) for h in COMMERCIAL) and "no-archive" not in r.tags:
            problems.append(f"{r.path.name}: {host} is a commercial prep site — tag it no-archive")
    return problems


def main(argv: list[str]) -> int:
    project = load_project(ROOT, "system-design")
    errors = project.card_errors + project.reading_errors + project.drill_errors
    leaves = [l.id for l in project.skeleton.leaves() if l.id.startswith(BRANCH + ".")]
    wanted = leaves if argv == ["--all"] else argv
    failed = 0
    for leaf_id in wanted:
        if leaf_id not in leaves:
            print(f"FAIL {leaf_id}: not a leaf under `{BRANCH}`")
            failed += 1
            continue
        found = check(project, leaf_id) + [e for e in errors if leaf_id.rsplit(".", 1)[-1] in e]
        print(f"{'FAIL' if found else 'ok  '} {leaf_id}" + "".join(f"\n       - {p}" for p in found))
        failed += bool(found)
    print(f"{len(wanted) - failed}/{len(wanted)} problem(s) pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
