"""q41 Observability Metrics — YOUR implementation.

RECONSTRUCTED TRAINING PROBLEM — see problem.md's warning block. Not a real Stripe question.

Input shape (see problem.md): stdin is `PART n`, then cumulative sections in this fixed order:
`WINDOW <size> <step>` (Part 2+), `RULES` rows (Part 3+), `LATENESS <L>` (Part 4 only), then
`EVENTS` rows (`timestamp,metric_name,labels,value`) for every part.
"""

from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """Parse EVENTS, group by (metric_name, canonical_labels). One line per group, sorted by
    metric_name then labels: '<metric>,<labels> count=<c> sum=<s> avg=<a>', then 'MALFORMED <n>'."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """WINDOW <size> <step> then EVENTS. One line per (metric,labels,window k) with >=1 event,
    sorted by metric, labels, k: '<metric>,<labels>,window=<k> count=<c> avg=<a> p50=<p> p90=<q>'
    (nearest-rank percentiles), then 'MALFORMED <n>'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """WINDOW, RULES, EVENTS. Per rule (in RULES order), walk every window 0..max_k and run the
    trigger_n/clear_n hysteresis state machine; emit only the transition lines
    ('<metric>,<labels> ALERT_ON window=<k>' / 'ALERT_OFF'), then 'MALFORMED <n>'."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """WINDOW, RULES, LATENESS, EVENTS (processed in arrival order, not sorted by timestamp).
    Drop events whose primary bucket (timestamp // step) is behind the watermark
    (max_primary_seen - L), then run Part 3's exact rule evaluation over what's left.
    Same transition-line output, then 'DROPPED <n>', then 'MALFORMED <n>'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not raw:
        return
    part = int(raw[0].split()[1])
    fn = {1: part1, 2: part2, 3: part3, 4: part4}[part]
    out = fn(raw[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
