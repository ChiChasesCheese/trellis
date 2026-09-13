#!/usr/bin/env python3
"""校验 loop/tree/interview-loop.yaml（受限 YAML，不依赖 PyYAML）。

  python3 loop/tree/check_tree.py            # 缺失路径 = warning，退出 0
  python3 loop/tree/check_tree.py --strict   # 缺失路径 = error，退出 1
  python3 loop/tree/check_tree.py --catalog  # 另检查 loop/CATALOG.md 是否含全部 problem ID
  python3 loop/tree/check_tree.py --tree-md  # 另检查 loop/tree/TREE.md 是否含全部 round/skill/problem ID

检查项：
  1. 每个 `problems: [..]` 里的 ID 能唯一解析到 loop/rounds/<round>/<id>_* 目录，
     非编码轮 ID（rc/hm/bq）解析到 loop/rounds/01_recruiter|02_hm|08_behavioral/bank.json
  2. 每个 `study: [..]` / `cards: [..]` 路径存在于 loop/ 下
  3. round `id` 对应 loop/rounds/<id>/ 目录存在
  4. 同一 round 内 skill id 不重复；problem ID 至少被一个 skill 引用一次（信息性）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LOOP = Path(__file__).resolve().parents[1]
ROUNDS = LOOP / "rounds"
YAML = LOOP / "tree" / "interview-loop.yaml"
NONCODE = {"rc": "01_recruiter", "hm": "02_hm", "bq": "08_behavioral"}

_LIST = re.compile(r"^\s*(problems|study|cards):\s*\[(.*)\]\s*$")
_ID = re.compile(r"^(\s*)-\s*id:\s*(\S+)\s*$")


def parse(text: str):
    """返回 (rounds, prereq_paths)。rounds = [{id, skills:[{id, problems}], study}]"""
    rounds, prereq, cur_round, cur_skill = [], [], None, None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = _ID.match(line)
        if m:
            indent, ident = len(m.group(1)), m.group(2)
            if indent == 2:
                cur_round = {"id": ident, "skills": [], "study": []}
                rounds.append(cur_round)
                cur_skill = None
            elif indent == 6 and cur_round is not None:
                cur_skill = {"id": ident, "problems": []}
                cur_round["skills"].append(cur_skill)
            continue
        m = _LIST.match(line)
        if m:
            key, items = m.group(1), [s.strip() for s in m.group(2).split(",") if s.strip()]
            if key == "problems" and cur_skill is not None:
                cur_skill["problems"].extend(items)
            elif key in ("study", "cards"):
                (cur_round["study"] if cur_round is not None else prereq).extend(items)
    return rounds, prereq


def resolve(pid: str) -> Path | None:
    if pid in NONCODE:
        p = ROUNDS / NONCODE[pid] / "bank.json"
        return p if p.exists() else None
    hits = list(ROUNDS.glob(f"*/{pid}_*"))
    return hits[0] if len(hits) == 1 else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--catalog", action="store_true")
    ap.add_argument("--tree-md", action="store_true")
    a = ap.parse_args()

    rounds, prereq = parse(YAML.read_text(encoding="utf-8"))
    errors, warnings = [], []
    all_pids: set[str] = set()

    for r in rounds:
        if not (ROUNDS / r["id"]).is_dir():
            warnings.append(f"round dir missing: rounds/{r['id']}")
        seen = set()
        for s in r["skills"]:
            if s["id"] in seen:
                errors.append(f"duplicate skill id in {r['id']}: {s['id']}")
            seen.add(s["id"])
            for pid in s["problems"]:
                all_pids.add(pid)
                if resolve(pid) is None:
                    warnings.append(f"problem not resolvable: {pid} (skill {r['id']}/{s['id']})")
        for path in r["study"]:
            if not (LOOP / path).exists():
                warnings.append(f"study path missing: {path} (round {r['id']})")
    for path in prereq:
        if not (LOOP / path).exists():
            warnings.append(f"prereq path missing: {path}")

    if a.catalog:
        cat = LOOP / "CATALOG.md"
        if not cat.exists():
            errors.append("CATALOG.md missing")
        else:
            text = cat.read_text(encoding="utf-8")
            for pid in sorted(all_pids):
                if not re.search(rf"\|\s*{re.escape(pid)}\s*\|", text):
                    errors.append(f"CATALOG.md lacks row for {pid}")
    if a.tree_md:
        md = LOOP / "tree" / "TREE.md"
        if not md.exists():
            errors.append("TREE.md missing")
        else:
            text = md.read_text(encoding="utf-8")
            for r in rounds:
                if r["id"] not in text:
                    errors.append(f"TREE.md lacks round {r['id']}")
                for s in r["skills"]:
                    if s["id"] not in text:
                        errors.append(f"TREE.md lacks skill {s['id']}")
            for pid in sorted(all_pids):
                if pid not in text:
                    errors.append(f"TREE.md lacks problem {pid}")

    if a.strict:
        errors, warnings = errors + warnings, []
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(
        f"rounds={len(rounds)} skills={sum(len(r['skills']) for r in rounds)} problems={len(all_pids)} "
        f"errors={len(errors)} warnings={len(warnings)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
