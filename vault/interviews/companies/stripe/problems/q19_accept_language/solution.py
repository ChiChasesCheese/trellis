"""q19 Accept-Language — reference solution.

Each header entry is (tag, q, position). For every supported tag the MOST SPECIFIC matching
entry decides its q (exact > language-only > '*'; ties by header position). Tags are then
emitted in descending q, ties by header position, then supported order; q=0 tags are dropped
(or appended last with zero_q="last").
"""
from __future__ import annotations

import sys


def _entries(header: str) -> list[tuple[str, float, int]]:
    """'en-US, fr;q=0.8' -> [('en-us', 1.0, 0), ('fr', 0.8, 1)]; lowercase, trimmed, blanks dropped."""
    out = []
    for pos, raw in enumerate(header.split(",")):
        parts = [p.strip() for p in raw.split(";")]
        tag = parts[0].lower()
        if not tag:
            continue
        q = 1.0  # default quality
        for p in parts[1:]:
            k, _, v = p.partition("=")
            if k.strip().lower() == "q":
                try:
                    q = float(v)
                except ValueError:
                    q = 1.0  # unparsable q -> default
        out.append((tag, q, pos))
    return out


def parse_accept_language(header: str, supported: list[str], zero_q: str = "exclude") -> list[str]:
    # supported: keep first spelling of each tag, in server order
    canon: dict[str, str] = {}
    for s in supported:
        s = s.strip()
        if s and s.lower() not in canon:
            canon[s.lower()] = s

    entries = _entries(header)
    ranked: list[tuple[float, int, int, str]] = []  # (-q, header pos, supported idx, tag)
    for idx, s in enumerate(canon):
        lang = s.split("-", 1)[0]
        best = None  # (specificity, -pos) -> the MOST SPECIFIC entry decides, ties by header position
        for tag, q, pos in entries:
            if tag == s:
                spec = 2  # exact tag
            elif tag == lang:
                spec = 1  # language-only tag ('fr' covers fr-CA, fr-FR)
            elif tag == "*":
                spec = 0  # wildcard: everything not covered by an explicit entry
            else:
                continue
            if best is None or (spec, -pos) > (best[0], -best[1]):
                best = (spec, pos, q)
        if best is not None:
            ranked.append((-best[2], best[1], idx, s))
    ranked.sort()  # rule: q descending, then header position, then supported order
    accepted = [t for nq, _, _, t in ranked if -nq > 0]
    if zero_q == "last":  # variant: q=0 tags sink to the end instead of being dropped
        accepted += [t for nq, _, _, t in ranked if -nq <= 0]
    return [canon[t] for t in accepted]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    header = lines[0] if lines else ""
    supported = [t.strip() for t in (lines[1] if len(lines) > 1 else "").split(",") if t.strip()]
    out = parse_accept_language(header, supported) or ["NONE"]
    stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
