"""Write the local index note of the whole design bank: every question and where it is covered.

    python3 research/hello-interview/gen_index.py prepare   # -> sources/local/.../index_todo.json, what a script cannot map
    python3 research/hello-interview/gen_index.py render    # -> vault/domains/hello-interview/premium/question-bank-index.md

Mapped by script: a question with a course breakdown, one with an answer in the selection files. The rest are assigned by
an agent in sources/local/.../index_map.json as {slug: "<target id>"}. The note and its data stay out of git: they come from
the logged-in bank.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / "sources/local/hello-interview/premium"
TYPES = {"SYSTEM_DESIGN": "系统设计", "OBJECT_ORIENTED_DESIGN": "低层设计"}


def bank() -> list[dict]:
    qs = json.loads((LOCAL / "questions.json").read_text(encoding="utf-8"))
    return sorted((q for q in qs if q["defaultInterviewType"] in TYPES), key=lambda q: -len(q.get("upvotes") or []))


def direct() -> dict[str, str]:
    out = {q["slug"]: f"answer:{q.get('body_slug', q['slug'])}" for q in json.loads((ROOT / "research/hello-interview/qb_selection.json").read_text(encoding="utf-8"))}
    more = json.loads((ROOT / "research/hello-interview/more_selection.json").read_text(encoding="utf-8"))["questions"]
    out.update({q["slug"]: f"answer:{q['slug']}" for q in more})
    return out


def targets() -> dict[str, str]:
    """Everything a question can point at, with a readable title."""
    sk = (ROOT / "skeleton/hello-interview.yaml").read_text(encoding="utf-8")
    titles = dict(re.findall(r"id: ((?:sd|lld)\.[\w-]+\.[\w-]+)\n\s+title: (.+)", sk))
    out = {k: v for k, v in titles.items() if ".cross." not in k}
    out.update({k: "跨题模式 · " + v for k, v in titles.items() if ".cross." in k})
    for f in sorted((ROOT / "vault/interviews/core/design-questions").glob("*.md")):
        m = re.search(r"^\*\*(.+?)\*\*", f.read_text(encoding="utf-8"), re.M)
        out[f"answer:{f.stem}"] = m.group(1) if m else f.stem
    for f in sorted((ROOT / "vault/domains/hello-interview/premium/bodies").glob("*.md")):
        m = re.search(r"^\*\*(.+?)\*\*", f.read_text(encoding="utf-8"), re.M)
        out[f"answer:{f.stem}"] = m.group(1) if m else f.stem
    for f in sorted((ROOT / "vault/domains/low-level-design/problems").glob("*/solution.py")):
        out[f"drill:{f.parent.name}"] = f"练习题 {f.parent.name}"
    for f in sorted((ROOT / "vault/interviews/core/low-level-design/problems").glob("*/solution.py")):
        out[f"drill:{f.parent.name}"] = f"练习题 {f.parent.name}"
    return out


def breakdown(q: dict) -> str | None:
    link = q.get("detailsLink") or ""
    m = re.search(r"/learn/(system-design|low-level-design)/problem-breakdowns/([\w-]+)", link)
    if not m:
        return None
    return f"{'sd' if m.group(1) == 'system-design' else 'lld'}.problem-breakdowns.{m.group(2)}"


def prepare() -> None:
    d = direct()
    todo = [{"slug": q["slug"], "title": q["title"], "type": TYPES[q["defaultInterviewType"]], "reports": len(q.get("upvotes") or []),
             "description": (q.get("description") or "")[:200]} for q in bank() if q["slug"] not in d and not breakdown(q)]
    (LOCAL / "index_todo.json").write_text(json.dumps({"targets": targets(), "questions": todo}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(len(bank()), "questions;", len(todo), "to map")


def render() -> None:
    d, tg = direct(), targets()
    manual = json.loads((LOCAL / "index_map.json").read_text(encoding="utf-8"))
    rows = {"系统设计": [], "低层设计": []}
    missing = 0
    for q in bank():
        ups = q.get("upvotes") or []
        last = max((u.get("approxAskedOn") or "")[:7] for u in ups) if ups else ""
        target = d.get(q["slug"]) or breakdown(q) or manual.get(q["slug"], "")
        if target not in tg:
            missing += 1
        url = f"https://www.hellointerview.com/community/questions/{q['slug']}/{q['id']}"
        rows[TYPES[q["defaultInterviewType"]]].append(f"| [{q['title']}]({url}) | {len(ups)} | {last} | {tg.get(target, '')} |")
    out = ["# 设计题全题库索引", "", "按被报告次数排序。最后一列是复习它时该看的材料。", ""]
    for name, lines in rows.items():
        out += [f"## {name}（{len(lines)} 题）", "", "| 题目 | 次数 | 最近 | 看哪里 |", "|---|---|---|---|", *lines, ""]
    path = ROOT / "vault/domains/hello-interview/premium/question-bank-index.md"
    path.write_text("\n".join(out), encoding="utf-8")
    print(sum(len(v) for v in rows.values()), "rows;", missing, "without a valid target")


if __name__ == "__main__":
    {"prepare": prepare, "render": render}[sys.argv[1]]()
