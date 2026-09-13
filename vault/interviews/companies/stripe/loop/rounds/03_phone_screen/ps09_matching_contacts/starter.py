"""ps09 Matching Contacts — YOUR implementation."""

from __future__ import annotations

import sys


def part1(rows: list[dict], weights: dict[str, float], threshold: float, target_user_id: str) -> list[str]:
    """rows: list of {'id','name','email','company'} dicts. weights: field -> weight. Two records
    are linked when the sum of weights of their exactly-equal, non-empty fields >= threshold.
    Return record ids directly linked (1 hop) to target_user_id, ascending, excluding the target."""
    # TODO
    return []


def part2(rows: list[dict], weights: dict[str, float], threshold: float, target_user_id: str) -> list[str]:
    """Same linkage rule as part1. Return record ids within <= 2 hops of target_user_id (direct
    links, plus links of those links), ascending, excluding the target itself."""
    # TODO
    return []


def part3(rows: list[dict], weights: dict[str, float], threshold: float, target_user_id: str) -> list[str]:
    """Same linkage rule as part1. Return every record id in target_user_id's connected component
    (any number of hops), ascending, excluding the target itself."""
    # TODO
    return []


# ---------------------------------------------------------------- I/O
PARTS = {"PART 1": part1, "PART 2": part2, "PART 3": part3}


def _parse_weights(line: str) -> dict[str, float]:
    weights: dict[str, float] = {}
    for chunk in line.split(","):
        field, _, value = chunk.strip().partition("=")
        weights[field.strip()] = float(value)
    return weights


def _parse_rows(lines: list[str]) -> list[dict]:
    rows = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        rid, name, email, company = (p.strip() for p in raw.split(","))
        rows.append({"id": rid, "name": name, "email": email, "company": company})
    return rows


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines:
        return
    header = lines[0].strip()
    if header not in PARTS:
        raise ValueError(f"unknown header: {header!r}")
    target = lines[1].strip()
    threshold = float(lines[2].strip())
    weights = _parse_weights(lines[3])
    rows = _parse_rows(lines[5:])  # lines[4] is the 'id,name,email,company' header, skipped
    out_ids = PARTS[header](rows, weights, threshold, target)
    stdout.write((",".join(out_ids) if out_ids else "NONE") + "\n")


if __name__ == "__main__":
    main()
