"""Index what the LLD reference solutions actually use: which idiom, in which problem, on which line.

    python3 research/domains/python/craft_index.py     # -> research/domains/python/craft_index.json

The input for the coding-craft cards, so a claim such as "used by 12 problems" comes from the code and not from memory.
"""
from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BANKS = [ROOT / "vault/domains/low-level-design/problems", ROOT / "vault/interviews/core/low-level-design/problems"]
TEXT = {
    "clock-injection": r"\bclock\b\s*[:=]", "lazy-deletion": r"(?i)lazy|tombstone|stale", "condition-wait": r"\.wait\(|\.wait_for\(",
    "transition-table": r"(?i)transitions?\b|_ALLOWED|_NEXT\b", "idempotency": r"(?i)idempot", "version-cas": r"(?i)\bversion\b|expected_version|compare_and",
    "snapshot": r"(?i)snapshot", "lock-per-key": r"(?i)defaultdict\(threading|_locks\b|striped?", "callback-outside-lock": r"(?i)outside the lock|锁外",
    "topo-cycle": r"(?i)topolog|cycle|环", "recursive-descent": r"(?i)tokeni[sz]e|_parse_|peek\(", "event-replay": r"(?i)replay|重放|event_log|append_only|只追加",
    "money-integer": r"(?i)cents|quantize|ROUND_", "heap-tiebreak": r"heappush\(.*\(", "bisect-sorted": r"bisect\.|insort",
}


def features(tree: ast.AST) -> dict[str, list[int]]:
    out: dict[str, list[int]] = defaultdict(list)
    for n in ast.walk(tree):
        line = getattr(n, "lineno", 0)
        if isinstance(n, ast.Import):
            for a in n.names:
                out[f"import {a.name}"].append(line)
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                out[f"{n.module}.{a.name}"].append(line)
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            for d in n.decorator_list:
                out["@" + ast.unparse(d)[:50]].append(d.lineno)
            if isinstance(n, ast.FunctionDef) and re.fullmatch(r"__\w+__", n.name) and n.name != "__init__":
                out[n.name].append(line)
            if isinstance(n, ast.ClassDef):
                for b in n.bases:
                    if ast.unparse(b) in ("Protocol", "ABC", "Enum", "IntEnum", "StrEnum", "Exception", "NamedTuple"):
                        out[f"class({ast.unparse(b)})"].append(line)
        elif isinstance(n, ast.Match):
            out["match"].append(line)
        elif isinstance(n, (ast.Yield, ast.YieldFrom)):
            out["yield"].append(line)
        elif isinstance(n, ast.NamedExpr):
            out["walrus"].append(line)
        elif isinstance(n, ast.With):
            out["with " + ast.unparse(n.items[0].context_expr)[:30]].append(line)
    return out


def main() -> None:
    index: dict[str, dict[str, list[int]]] = defaultdict(dict)
    problems = []
    for bank in BANKS:
        for f in sorted(bank.glob("*/solution.py")):
            slug, src = f.parent.name, f.read_text(encoding="utf-8")
            problems.append({"slug": slug, "lines": src.count("\n"), "path": str(f.relative_to(ROOT))})
            for k, v in features(ast.parse(src)).items():
                index[k][slug] = sorted(set(v))[:6]
            for k, pat in TEXT.items():
                hits = [i for i, x in enumerate(src.splitlines(), 1) if re.search(pat, x)]
                if hits:
                    index["~" + k][slug] = hits[:6]
    ranked = dict(sorted(index.items(), key=lambda kv: -len(kv[1])))
    out = ROOT / "research/domains/python/craft_index.json"
    out.write_text(json.dumps({"problems": problems, "index": ranked}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(len(problems), "problems;", len(ranked), "features")


if __name__ == "__main__":
    main()
