"""cd05 Business Account Data Verification — reference solution.

Rule engine over a nested JSON `account` object. See problem.md for the full path syntax
("." nesting, one `owners[]` wildcard segment per path), the "non-empty" definition, and the
`when` / `requires` / `one_of` semantics. Pure tree-walking, no regex, no external deps.
"""

from __future__ import annotations

import json
import sys
from typing import Any

MISSING = object()  # sentinel: a path did not resolve to any value at all


def _split(path: str) -> list[str]:
    """Split a "." path into segments, e.g. "owners[].first_name" -> ["owners[]", "first_name"]."""
    return path.split(".")


def _is_nonempty(value: Any) -> bool:
    """See problem.md '"非空"定义': only null / "" / [] count as empty. Everything else
    (numbers, booleans, empty dicts) counts as non-empty."""
    if value is MISSING or value is None:
        return False
    if isinstance(value, str):
        return value != ""
    if isinstance(value, list):
        return len(value) > 0
    return True


def _expand(node: Any, segments: list[str], prefix: str) -> list[tuple[str, Any]]:
    """Resolve `segments` (already split on '.') against `node`.

    Returns (resolved_path_string, value) pairs. A segment ending in '[]' iterates that array:
    zero elements yields nothing (vacuous truth); a missing/non-list base yields one pair with
    the *literal*, unexpanded remainder of the path and value=MISSING. A plain segment that
    can't be resolved similarly yields one literal/MISSING pair.
    """
    seg, rest = segments[0], segments[1:]
    literal_tail = ".".join([seg, *rest]) if rest else seg

    if seg.endswith("[]"):
        key = seg[:-2]
        arr = node.get(key) if isinstance(node, dict) else None
        if not isinstance(arr, list):
            return [(prefix + literal_tail, MISSING)]
        out: list[tuple[str, Any]] = []
        for i, elem in enumerate(arr):
            idx_seg = f"{key}[{i}]"
            if rest:
                out.extend(_expand(elem, rest, prefix + idx_seg + "."))
            else:
                out.append((prefix + idx_seg, elem))
        return out

    if not isinstance(node, dict) or seg not in node:
        return [(prefix + literal_tail, MISSING)]
    val = node[seg]
    if rest:
        return _expand(val, rest, prefix + seg + ".")
    return [(prefix + seg, val)]


def _resolve_one(node: Any, path: str) -> tuple[bool, Any]:
    """Single-value resolve for `when` conditions (no wildcards). Returns (exists, value)."""
    cur = node
    for seg in _split(path):
        if not isinstance(cur, dict) or seg not in cur:
            return False, None
        cur = cur[seg]
    return True, cur


def _when_matches(account: dict, conditions: list[dict]) -> bool:
    """AND over `conditions` (empty/omitted -> always matches); see problem.md "when"."""
    for cond in conditions:
        exists, value = _resolve_one(account, cond["path"])
        if "equals" in cond:
            if not (exists and value == cond["equals"]):
                return False
        elif "present" in cond:
            if exists != bool(cond["present"]):
                return False
    return True


def _missing_for_requires(account: dict, path: str) -> list[str]:
    """Expand `path` (wildcards included) and return the resolved tokens that are empty/missing."""
    return [
        resolved_path
        for resolved_path, value in _expand(account, _split(path), "")
        if not _is_nonempty(value)
    ]


def _missing_for_one_of(account: dict, paths: list[str]) -> str | None:
    """None if any path is non-empty, else the "one_of(a|b|...)" token in declaration order."""
    for path in paths:
        exists, value = _resolve_one(account, path)
        if exists and _is_nonempty(value):
            return None
    return "one_of(" + "|".join(paths) + ")"


def part1(doc: dict) -> list[str]:
    """Check every "requires" path across all rules; ["VERIFIED"] if all are non-empty."""
    account = doc.get("account", {})
    missing: set[str] = set()
    for rule in doc.get("rules", []):
        for path in rule.get("requires", []):
            missing.update(_missing_for_requires(account, path))
    return sorted(missing) if missing else ["VERIFIED"]


def part2(doc: dict) -> list[str]:
    """Same as part1, gated by "when" and adding "one_of" groups and "[]" wildcard paths."""
    account = doc.get("account", {})
    missing: set[str] = set()
    for rule in doc.get("rules", []):
        if not _when_matches(account, rule.get("when", [])):
            continue
        for path in rule.get("requires", []):
            missing.update(_missing_for_requires(account, path))
        one_of = rule.get("one_of")
        if one_of:
            token = _missing_for_one_of(account, one_of)
            if token is not None:
                missing.add(token)
    return sorted(missing) if missing else ["VERIFIED"]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text = stdin.read()
    header, _, rest = text.partition("\n")
    part = int(header.strip().split()[-1])
    doc = json.loads(rest)
    out = part1(doc) if part == 1 else part2(doc)
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
