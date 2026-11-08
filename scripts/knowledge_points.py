"""Write the exam-point map as two Obsidian outline notes, viewed as mind maps (Mindmap NextGen), like the knowledge trees.

    uv run python scripts/knowledge_points.py

`系统设计 考点地图`: group -> topic -> its exam points, heaviest first, with how many questions need each and how.
`系统设计 题目考点`: group -> question -> the points its answer needs, by role, then its own points.
Titles and counts only: nothing about the learner, and no card text. Weak-spot topics from the learner's own mock are left
out. Regenerate after exam points change (research/sysdesign/KP_AGENT.md).
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import plan_kp  # noqa: E402
import study_plan as S  # noqa: E402

OUT = ROOT / "vault/domains/hello-interview"
FOLD = " <!-- markmap: fold -->"
PERSONAL = {"s00"}  # weak spots from the learner's own mock interview
ROLES = ("必讲", "追问", "加分")


def clean(title: str) -> str:
    return re.sub(r"\s+", " ", title.replace("<", "＜").replace(">", "＞").replace("|", "/")).strip()


def main() -> int:
    S.cfg_global.update(S.config())
    tree = S.Tree()
    cards, _, base, _ = S.build_inputs(tree)
    pts, w = S.kp_state["points"], S.kp_state["weight"]
    req = plan_kp.required_by(pts)
    topics_in_order = list(dict.fromkeys(c.topic for c in cards))
    groups = defaultdict(list)
    for t in topics_in_order:
        if tree.top(t) not in PERSONAL:
            groups[tree.top(t)].append(t)
    by_topic = defaultdict(list)
    for k, m in pts.meta.items():
        if k not in plan_kp.META:
            by_topic[m["topic"]].append(k)

    concepts, questions = ["# 系统设计 考点地图", ""], ["# 系统设计 题目考点", ""]
    n_points, n_questions = 0, 0
    for g in sorted(groups):
        ts = [t for t in groups[g] if t not in pts.needs and by_topic.get(t)]
        if ts:
            concepts.append(f"- {clean(tree.title(g))}")
            for t in sorted(ts, key=lambda t: -sum(w[k] for k in by_topic[t])):
                ks = sorted(by_topic[t], key=lambda k: -w[k])
                concepts.append(f"  - {clean(tree.title(t))} · {len(ks)}{FOLD}")
                for k in ks:
                    n = Counter(r[1] for r in req.get(k, []))
                    how = " ".join(f"{role}{n[role]}" for role in ROLES if n[role])
                    concepts.append(f"    - {'★ ' if pts.meta[k].get('core') else ''}{clean(pts.meta[k]['title'])}{' · ' + how if how else ''}")
                    n_points += 1
        qs = [t for t in groups[g] if t in pts.needs and t not in S.NOT_A_QUESTION]
        if qs:
            questions.append(f"- {clean(tree.title(g))}")
            for q in sorted(qs, key=lambda q: -base.get(q, 0.0)):
                questions.append(f"  - {clean(tree.title(q))}{FOLD}")
                n_questions += 1
                for role in ROLES:
                    ks = sorted((n["kp"] for n in pts.needs[q] if n["role"] == role), key=lambda k: -w[k])
                    if ks:
                        questions.append(f"    - {role} · {len(ks)}")
                        questions += [f"      - {clean(pts.meta[k]['title'])}" for k in ks]
                own = pts.own.get(q, [])
                if own:
                    questions.append(f"    - 本题专属 · {len(own)}")
                    questions += [f"      - {clean(o['title'])}" for o in own]
    (OUT / "系统设计 考点地图.md").write_text("\n".join(concepts) + "\n", encoding="utf-8")
    (OUT / "系统设计 题目考点.md").write_text("\n".join(questions) + "\n", encoding="utf-8")
    print(f"{n_points} points, {n_questions} questions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
