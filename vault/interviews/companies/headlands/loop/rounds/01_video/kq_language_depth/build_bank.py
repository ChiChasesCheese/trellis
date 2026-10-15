#!/usr/bin/env python3
"""Generate bank.json from questions.md (do not hand-edit bank.json).

Usage:  python3 build_bank.py            # writes bank.json next to this file, prints counts per topic
Checks: every question has difficulty, source, one-line answer, expansion, 60-second version, follow-ups;
        every demo file named in a 'Demo / 课文' line exists under demos/.
Exit code 1 if any check fails.
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "questions.md"
OUT = HERE / "bank.json"

TOPIC_RE = re.compile(r"^## \[(?P<key>[A-Z])\] (?P<name>.+?)\s*$")
Q_RE = re.compile(r"^### Q(?P<n>\d+) · (?P<q>.+?)\s*$")
DIFF_RE = re.compile(r"^- \*\*难度\*\*：(?P<stars>★+)")
SRC_RE = re.compile(r"^- \*\*来源\*\*：(?P<src>.+)$")
ANS_RE = re.compile(r"^- \*\*一句话答案\*\*：(?P<ans>.+)$")
DEMO_RE = re.compile(r"^\*\*Demo / 课文\*\*：(?P<rest>.+)$")
LEVEL = {1: "easy", 2: "medium", 3: "hard"}


def main() -> int:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    questions = []
    topic = None
    cur = None
    errors = []

    def close():
        nonlocal cur
        if cur is not None:
            questions.append(cur)
            cur = None

    for line in lines:
        m = TOPIC_RE.match(line)
        if m:
            close()
            topic = f"{m['key']} {m['name']}"
            continue
        m = Q_RE.match(line)
        if m:
            close()
            cur = {"id": f"kqld-{int(m['n']):02d}", "topic": topic, "question": m["q"],
                   "difficulty": None, "stars": None, "source": None, "short_answer": None,
                   "inferred": False, "source_kind": None, "demos": [], "has": set()}
            continue
        if cur is None:
            continue
        if line.startswith("---"):
            continue
        if (m := DIFF_RE.match(line)):
            cur["stars"] = len(m["stars"])
            cur["difficulty"] = LEVEL[len(m["stars"])]
        elif (m := SRC_RE.match(line)):
            cur["source"] = m["src"].strip()
            cur["inferred"] = "推断" in m["src"]
            cur["source_kind"] = ("cpp-translation" if "推断：Java 对应" in m["src"]
                                  else "jd" if "推断：JD" in m["src"]
                                  else "java-classic" if "推断：Java 低延迟岗经典" in m["src"] else "other")
        elif (m := ANS_RE.match(line)):
            cur["short_answer"] = m["ans"].strip()
        elif (m := DEMO_RE.match(line)):
            cur["has"].add("demoline")
            cur["demos"] = sorted(set(re.findall(r"demos/(K\d+\w*\.java|run_tools\.sh|OUTPUTS\.txt)", m["rest"])))
        elif line.startswith("**展开**"):
            cur["has"].add("expand")
        elif line.startswith("**能说出口的 60 秒版本**"):
            cur["has"].add("sixty")
        elif line.startswith("**面试官可能的下一问**"):
            cur["has"].add("followups")
    close()

    for q in questions:
        for field in ("topic", "difficulty", "source", "short_answer"):
            if not q[field]:
                errors.append(f"{q['id']}: missing {field}")
        for need in ("expand", "sixty", "followups"):
            if need not in q["has"]:
                errors.append(f"{q['id']}: missing section {need}")
        for d in q["demos"]:
            if not (HERE / "demos" / d).exists():
                errors.append(f"{q['id']}: demo not found: demos/{d}")
        if "demoline" not in q["has"]:
            errors.append(f"{q['id']}: no 'Demo / 课文' line")
    ids = [q["id"] for q in questions]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids")

    bank = [{"id": q["id"], "topic": q["topic"], "difficulty": q["difficulty"], "stars": q["stars"],
             "question": q["question"], "short_answer": q["short_answer"],
             "source": q["source"], "source_kind": q["source_kind"], "inferred": q["inferred"], "demos": q["demos"]}
            for q in questions]
    OUT.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = OrderedDict()
    for q in questions:
        counts[q["topic"]] = counts.get(q["topic"], 0) + 1
    print(f"{len(questions)} questions -> {OUT.name}")
    for t, c in counts.items():
        print(f"  {c:2d}  {t}")
    by_diff = OrderedDict((d, sum(1 for q in questions if q["difficulty"] == d)) for d in LEVEL.values())
    print("  difficulty:", dict(by_diff))
    kinds = OrderedDict()
    for q in questions:
        kinds[q["source_kind"]] = kinds.get(q["source_kind"], 0) + 1
    print("  source kinds:", dict(kinds))
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  -", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
