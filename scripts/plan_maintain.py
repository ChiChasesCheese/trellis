"""Keep the planner's annotations in step with new cards. Run by the daily job before the plan.

    uv run python scripts/plan_maintain.py          # refresh LeetCode sections; report what still needs annotating
    uv run python scripts/plan_maintain.py export   # also write the input files for the annotating agent

LeetCode: sources/local/lc/sections.jsonl (一句话 / 识别 / 易错点 of each body) and same.json (the numbers each body lists
under 同模式) are rebuilt from vault/interviews/core/leetcode/problems/. A problem with no tags is listed.
System design: a card with no exam points is listed. Agents annotate both: research/lc-analysis/CLASSIFY_AGENT.md and
research/sysdesign/KP_AGENT.md ("New cards").
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from lc_data import LC, OUT as LC_OUT  # noqa: E402

KP = ROOT / "sources/local/plan/kp"


def section(body: str, name: str) -> str:
    m = re.search(rf"^\*\*{name}。\*\*(.*?)(?=^\*\*[^*\n]{{1,12}}。\*\*|\Z)", body, re.M | re.S)
    return m.group(1).strip() if m else ""


def refresh_sections() -> list[str]:
    """Rewrite sections.jsonl and same.json; returns slugs with no technique tag."""
    rows, same = [], {}
    for f in sorted((LC / "problems").glob("*.md")):
        text = f.read_text(encoding="utf-8")
        t = re.search(r"^\*\*(LC \d+[^*]*?)\*\*", text, re.M)
        title = t.group(1).strip() if t else f.stem
        rows.append({"slug": f.stem, "title": title, "idea": section(text, "一句话"), "signal": section(text, "识别"),
                     "pitfalls": section(text, "易错点")})
        same[f.stem] = sorted({int(n) for n in re.findall(r"LC\s*(\d+)", section(text, "同模式"))})
    (LC_OUT / "sections.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    (LC_OUT / "same.json").write_text(json.dumps(same, ensure_ascii=False, indent=0), encoding="utf-8")
    tagged = set()
    for f in LC_OUT.glob("tags_*.jsonl"):
        for line in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r.get("techniques"):
                tagged.add(r["slug"])
    return [r["slug"] for r in rows if r["slug"] not in tagged]


def untagged_cards(export: bool) -> dict[str, list[str]]:
    """Topic -> system-design card ids with no exam-point mapping."""
    import plan_kp
    import study_plan as S
    pts = plan_kp.load()
    tree = S.Tree()
    cards, *_ = S.build_inputs(tree)
    out: dict[str, list[str]] = {}
    for c in cards:
        if c.id not in pts.card:
            out.setdefault(c.topic, []).append(c.id)
    if export and out:
        raw = {c.id: c for c in tree.project.cards}
        folder = KP / "new"
        folder.mkdir(parents=True, exist_ok=True)
        txt = lambda x: re.sub(r"\s+", " ", x or "").strip()
        for t, ids in out.items():
            doc = {"topic": t, "title": tree.title(t), "question": S.question_topic(tree, t),
                   "cards": [{"id": i, "q": txt(raw[i].question)[:300],
                              "a": txt((raw[i].answer or "") + " " + (getattr(raw[i], "text", "") or ""))[:600]} for i in ids]}
            (folder / f"{t}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=0), encoding="utf-8")
    return out


def main() -> int:
    missing = refresh_sections()
    print(f"LeetCode problems with no tags: {len(missing)}" + (f" ({', '.join(missing[:10])})" if missing else ""))
    cards = untagged_cards("export" in sys.argv)
    dag_file = KP / "dag.json"
    if dag_file.exists():
        known = {k["id"] for v in json.loads((KP / "catalog.json").read_text(encoding="utf-8")).values() for k in v}
        level = json.loads(dag_file.read_text(encoding="utf-8")).get("level", {})
        print(f"exam points not yet placed in the prerequisite DAG: {len(known - set(level))}")
    n = sum(len(v) for v in cards.values())
    print(f"system-design cards with no exam points: {n} in {len(cards)} topics" + (f" ({', '.join(list(cards)[:10])})" if cards else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
