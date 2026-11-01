"""Pick the high-frequency questions from the public question bank and prepare their sources and deck stubs.

    uv run python research/hello-interview/build_qb.py    # then gen_skeleton.py

Selection (80/20 on report counts): the 30 most-reported system design questions (~96% of visible reports) and every
object-oriented / low-level design question. Each question gets:
- a source file sources/local/hello-interview/qb/<slug>.md: the question, every report's note (company, level,
  month), and the free problem-breakdown page text when Hello Interview has one (gitignored);
- a stub card vault/domains/hello-interview/cards/qb/<sd|lld>/hi-qb-<slug>.md over the shared body
  vault/interviews/core/design-questions/<slug>.md (written by the QB card agents), meta = report facts.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sources/local/hello-interview"
TOP_SD = 30


def main() -> None:
    full = {q["id"]: q for q in json.loads((SRC / "questions.json").read_text(encoding="utf-8"))}
    slim = json.loads((ROOT / "research/hello-interview/questions.json").read_text(encoding="utf-8"))["questions"]
    sd = [q for q in slim if q["type"] in ("SYSTEM_DESIGN", "PRODUCT_DESIGN")][:TOP_SD]
    lld = [q for q in slim if q["type"] == "OBJECT_ORIENTED_DESIGN"]
    sel = []
    (SRC / "qb").mkdir(parents=True, exist_ok=True)
    for track, qs in (("sd", sd), ("lld", lld)):
        for q in qs:
            f = full[q["id"]]
            notes = [f"- {u.get('company') or '?'} · {u.get('level') or '?'} · {(u.get('approxAskedOn') or '')[:7]}"
                     + (f"：{u['description']}" if u.get("description") else "") for u in f.get("upvotes") or []]
            text = f"# {q['title']}\n\n{f.get('description') or ''}\n\n## Reports ({len(notes)})\n" + "\n".join(notes)
            if q["breakdown"]:
                page = SRC / (q["breakdown"].removeprefix("/learn/").replace("/", "__") + ".md")
                if page.exists() and page.stat().st_size > 12000:  # a free breakdown, not a premium preview
                    text += "\n\n## Problem breakdown (Hello Interview)\n\n" + page.read_text(encoding="utf-8")
            (SRC / "qb" / f"{q['slug']}.md").write_text(text, encoding="utf-8")
            levels = sorted({u.get("level") for u in f.get("upvotes") or [] if u.get("level")})
            sel.append({**q, "track": track, "levels": levels})
            stub = ROOT / f"vault/domains/hello-interview/cards/qb/{track}/hi-qb-{q['slug']}.md"
            stub.parent.mkdir(parents=True, exist_ok=True)
            comp = "、".join(q["companies"][:5]) + (" 等" if len(q["companies"]) > 5 else "")
            meta = f"被报告 {q['reports']} 次" + (f" · {comp}" if comp else "") + (f" · 最近 {q['last'][:7]}" if q["last"] else "")
            stub.write_text(f"---\nid: hi-qb-{q['slug']}\nnode: qb.{track}.{q['slug']}\ntype: qa\n"
                            f"body: interviews/core/design-questions/{q['slug']}\nmeta: {json.dumps(meta, ensure_ascii=False)}\n---\n",
                            encoding="utf-8")
    (ROOT / "research/hello-interview/qb_selection.json").write_text(json.dumps(sel, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(sd), "system design +", len(lld), "low-level design questions")


if __name__ == "__main__":
    main()
