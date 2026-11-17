"""Format review of the psych cards against CARDS_TASK.md: what a script can check before a person reads them.

    python3 research/domains/psych/review.py            # every defect, then the totals
    python3 research/domains/psych/review.py --dump B   # print group B's cards as plain text for reading
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_tree  # noqa: E402

ROOT = gen_tree.ROOT
CARDS = ROOT / "vault/domains/psych/cards"
GRADE_TAG = {"A": "证据强", "B": "证据中", "C": "证据弱"}
TAG_WORD = {"证据强": "强", "证据中": "中", "证据弱": "弱"}
BANNED = ["研究表明", "科学家发现", "据报道", "你并不孤单", "请记住", "要记住", "总之", "所以说", "值得注意", "需要注意",
          "http", "来源", "见上一张", "如前所述", "小明", "有一位", "意识到这一点", "保持开放", "心态", "众所周知", "不妨"]
FIGURE = re.compile(r"^```mermaid|^<svg\b", re.M)
STRIP = re.compile(r"^```.*?^```|^<svg\b.*?</svg>|^\|.*$", re.S | re.M)


def han(text: str) -> int:
    return sum(1 for ch in text if "一" <= ch <= "鿿")


def main(argv: list[str]) -> int:
    leaves = {leaf["id"]: leaf for top in gen_tree.parse() for mid in top["children"] for leaf in mid["children"]}
    core = {gen_tree.card_id(i): leaf for i, leaf in leaves.items() if leaf["core"]}
    dump = argv[1] if len(argv) == 2 and argv[0] == "--dump" else None
    found, figures, defects = set(), 0, 0
    seen_file = Path("/tmp/psy_reviewed.txt")  # ids already read by the reviewer: --dump prints only the rest
    seen = set(seen_file.read_text().split()) if seen_file.exists() else set()
    shown: list[str] = []
    for path in sorted(CARDS.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n## Q\n(.*?)\n## A\n(.*)", text, re.S)
        problems: list[str] = []
        if not m:
            print(f"{path.name}: not in the card layout")
            defects += 1
            continue
        front, question, answer = m.groups()
        cid = re.search(r"^id: (.+)$", front, re.M).group(1).strip()
        node = re.search(r"^node: (.+)$", front, re.M).group(1).strip()
        tags = re.search(r"^tags: \[(.*)\]$", front, re.M)
        tags = [t.strip() for t in tags.group(1).split(",")] if tags else []
        found.add(cid)
        leaf = core.get(cid)
        if cid != path.stem:
            problems.append("id differs from the file name")
        if leaf is None:
            problems.append("not a core leaf")
        elif leaf["id"] != node:
            problems.append(f"node should be {leaf['id']}")
        grade_tags = [t for t in tags if t in TAG_WORD]
        if len(grade_tags) != 1:
            problems.append("needs exactly one evidence tag")
        else:
            if f"**证据 · {TAG_WORD[grade_tags[0]]}：**" not in answer:
                problems.append("evidence line does not match the tag")
            if leaf and GRADE_TAG[leaf["grade"]] != grade_tags[0]:
                problems.append(f"grade changed: tree {leaf['grade']}, card {grade_tags[0]}")
        if leaf and ("十日终焉" in leaf["tags"]) != ("十日终焉" in tags):
            problems.append("十日终焉 tag differs from the tree")
        if not answer.lstrip().startswith("**"):
            problems.append("answer does not open with the bold sentence")
        if "**故事。**" not in answer:
            problems.append("no 故事")
        if "**动手：**" not in answer:
            problems.append("no 动手")
        size = han(STRIP.sub("", answer))
        if size > 400:
            problems.append(f"answer is {size} characters")
        if re.search(r"什么是|是什么[？?]\s*$", question.strip()) and han(question) < 25:
            problems.append("question is a bare definition")
        hits = [w for w in BANNED if w in question + STRIP.sub("", answer)]
        if hits:
            problems.append(f"banned words: {hits}")
        if FIGURE.search(answer):
            figures += 1
        if problems:
            defects += 1
            print(f"{path.name}: " + "; ".join(problems))
        if dump and leaf and gen_tree.group_of(leaf["id"]) == dump and cid not in seen:
            shown.append(cid)
            body = re.sub(r"^<svg\b.*?</svg>", "[svg]", answer, flags=re.S | re.M)
            print(f"\n===== {cid}  [{','.join(tags)}]  {size}字\nQ: {question.strip()}\n{body.strip()}")
    if dump:
        seen_file.write_text("\n".join(sorted(seen | set(shown))) + "\n")
    missing = sorted(set(core) - found)
    if not dump:
        print(f"\n{len(found)} cards, {figures} with a figure ({figures * 100 // max(len(found), 1)}%), "
              f"{defects} with defects, {len(missing)} core leaves without a card")
        by_group: dict[str, int] = {}
        for cid in missing:
            g = gen_tree.group_of(core[cid]["id"])
            by_group[g] = by_group.get(g, 0) + 1
        if missing:
            print("missing by group:", dict(sorted(by_group.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
