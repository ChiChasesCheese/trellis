"""Check one chunk of recognition questions written by a card agent, and merge its parts for import.

    uv run python scripts/recog_review.py 03            # checks; writes sources/local/quiz/recog-bulk-03.json when clean
    uv run python scripts/recog_review.py 03 --show     # also print every question on two lines, for reading

Checks against the chunk's todo file (sources/local/quiz/recog-todo-<date>-NN.md): every problem answered once, in
order, with the entry's topic and LC number; the importer's lint (per question and the length tell over the file); no
option repeated as filler across the chunk more than a few times. Leaf words on the front are listed as notes. The reading itself (is each wrong option really wrong?) stays with the orchestrator: `--show`.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import daily_quiz  # noqa: E402

HOME = ROOT / "sources/local/quiz"
GENERIC = {"基础", "进阶", "其他", "综合应用", "进阶（选做）", "遍历", "搜索", "思维题", "基础题"}   # leaf names that are not technique names


def entries(todo: Path) -> list[dict]:
    out = []
    for block in re.split(r"\n(?=- topic: )", todo.read_text(encoding="utf-8")):
        m = re.match(r"- topic: (\S+)\n  - 题目：(LC \d+)[^\n]*\n  - 所在叶子（不要写进题目）：([^\n]*)", block)
        if m:
            out.append({"topic": m.group(1), "lc": m.group(2), "leaf": [x.strip() for x in m.group(3).split("›")]})
    return out


def main() -> int:
    nn = sys.argv[1]
    todo = next(iter(sorted(HOME.glob(f"recog-todo-*-{nn}.md"))), None)
    if not todo:
        print(f"no todo file for chunk {nn}")
        return 2
    want = entries(todo)
    parts = sorted(HOME.glob(f"recog-bulk-{nn}.part*.json"))
    qs = [q for p in parts for q in json.loads(p.read_text(encoding="utf-8"))]
    problems, notes = [], []   # notes: worth a look, not blocking (a tree problem has to say 二叉树)
    if [q.get("topic") for q in qs] != [e["topic"] for e in want]:
        got, need = [q.get("topic") for q in qs], [e["topic"] for e in want]
        missing = [t for t in need if t not in got]
        extra = [t for t in got if t not in need]
        problems.append(f"topics differ from the todo file: {len(qs)} written, {len(want)} wanted; missing {missing[:5]}, "
                        f"extra {extra[:5]}{'' if missing or extra else ' (same set, different order)'}")
    by_topic = {e["topic"]: e for e in want}
    for i, q in enumerate(qs, 1):
        e = by_topic.get(q.get("topic"))
        if not e:
            continue
        if not q.get("title", "").startswith(e["lc"] + " "):
            problems.append(f"{i}: title {q.get('title', '')[:24]!r} is not {e['lc']}")
        front = q.get("statement", "") + q.get("question", "")
        for name in e["leaf"][1:]:   # the list's own title (链表、二叉树与回溯) names structures, not techniques
            for piece in re.split(r"[（）()/、 ]+", name):
                if len(piece) >= 3 and piece not in GENERIC and piece in front:
                    notes.append(f"{i}: {e['lc']} has a leaf word on the front: {piece!r}")
    for i, err in daily_quiz.lint_file(qs):
        problems.append(f"{i + 1 if i >= 0 else 'file'}: {err}")
    filler = collections.Counter(o for q in qs for k, o in enumerate(q.get("options", []))
                                 if k not in (q["correct"] if isinstance(q.get("correct"), list) else [q.get("correct")]))
    for o, n in filler.most_common(5):
        if n > max(4, len(qs) // 20):
            problems.append(f"file: the wrong option {o!r} is used {n} times: filler")
    single = [q for q in qs if isinstance(q.get("correct"), int)]
    longest = sum(1 for q in single if len(q["options"][q["correct"]]) > max(len(o) for k, o in enumerate(q["options"]) if k != q["correct"]))
    print(f"chunk {nn}: {len(qs)} questions in {len(parts)} part(s); {len(qs) - len(single)} multi-select; "
          f"correct option longest in {longest}/{len(single)}; {len(problems)} problem(s)")
    for p in problems:
        print("  ", p)
    for p in sorted(set(notes)):
        print("   note:", p)
    if "--show" in sys.argv:
        for i, q in enumerate(qs, 1):
            right = q["correct"] if isinstance(q["correct"], list) else [q["correct"]]
            print(f"{i}. {q['title']} ｜ {q['statement']} ｜ {q['question']}")
            print("   ✓ " + " + ".join(q["options"][k] for k in right) + " ✗ " + " / ".join(o for k, o in enumerate(q["options"]) if k not in right))
            print(f"   why: {q['why']} 〔{q['point']}〕")
    if not problems:
        (HOME / f"recog-bulk-{nn}.json").write_text(json.dumps(qs, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"merged -> sources/local/quiz/recog-bulk-{nn}.json")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
