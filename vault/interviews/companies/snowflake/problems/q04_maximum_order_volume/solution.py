"""q04 Maximum Order Volume — reference solution.

Weighted interval scheduling. Each call i occupies the half-open interval
[start[i], start[i] + duration[i]). Two calls are non-overlapping iff one's end
<= the other's start (touching endpoints do NOT conflict). Select a subset of
non-overlapping calls maximizing the sum of volume[i].

Standard approach: sort calls by end time; dp[k] = best achievable using only
the first k calls (in sorted order); for call k (1-indexed), find the largest
predecessor index pred such that ends[pred-1] <= starts[k-1] (0-indexed
arrays), then dp[k] = max(dp[k-1], volume[k-1] + dp[pred]).

A call with duration == 0 occupies the EMPTY interval [start, start): there is
no x with start <= x < start, so it never intersects any other interval no
matter where it sits, even one that "contains" its instant. This is a genuine
special case, not something the plain "end <= start" pairwise check derives
for free: e.g. a zero-duration call at t=5 and a normal call [0, 10) satisfy
neither `10 <= 5` nor `5 <= 0`, so the general pairwise check would (wrongly)
call them overlapping. We therefore strip zero-duration calls out, sum their
volumes unconditionally (call it `free`), and run the standard weighted
interval scheduling DP on only the positive-duration calls; the answer is
`free + dp`. Since volumes are non-negative, this matches "the optimal answer
must include ALL zero-duration calls automatically".

part1 is a correct-but-simple O(n^2)-worst-case version (linear predecessor
scan). part2 is the O(n log n) version required for n up to 1e5 (binary
search via bisect for the predecessor).
"""
from __future__ import annotations

import sys
from bisect import bisect_right


def _split_free_and_normal(start: list[int], duration: list[int], volume: list[int]):
    """Returns (free_volume_sum, start', duration', volume') where the primed
    lists contain only the positive-duration ("normal") calls; zero-duration
    calls are always includable, so their volumes are summed unconditionally."""
    free = 0
    ns: list[int] = []
    nd: list[int] = []
    nv: list[int] = []
    for s, d, v in zip(start, duration, volume):
        if d == 0:
            free += v
        else:
            ns.append(s)
            nd.append(d)
            nv.append(v)
    return free, ns, nd, nv


def _sorted_by_end(start: list[int], duration: list[int], volume: list[int]):
    n = len(start)
    order = sorted(range(n), key=lambda i: (start[i] + duration[i], start[i]))
    ends = [start[i] + duration[i] for i in order]
    starts = [start[i] for i in order]
    vols = [volume[i] for i in order]
    return ends, starts, vols


def part1(start: list[int], duration: list[int], volume: list[int]) -> int:
    """Correct DP, any complexity (here: sort by end + linear predecessor scan)."""
    free, start, duration, volume = _split_free_and_normal(start, duration, volume)
    n = len(start)
    if n == 0:
        return free
    ends, starts, vols = _sorted_by_end(start, duration, volume)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        pred = 0
        for j in range(i - 1, 0, -1):
            if ends[j - 1] <= starts[i - 1]:
                pred = j
                break
        dp[i] = max(dp[i - 1], vols[i - 1] + dp[pred])
    return free + dp[n]


def part2(start: list[int], duration: list[int], volume: list[int]) -> int:
    """Same semantics as part1, but O(n log n): sort by end + bisect for the
    latest non-overlapping predecessor."""
    free, start, duration, volume = _split_free_and_normal(start, duration, volume)
    n = len(start)
    if n == 0:
        return free
    ends, starts, vols = _sorted_by_end(start, duration, volume)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        # largest count of calls among ends[0:i-1] with end <= starts[i-1]
        pred = bisect_right(ends, starts[i - 1], 0, i - 1)
        dp[i] = max(dp[i - 1], vols[i - 1] + dp[pred])
    return free + dp[n]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip() != ""]
    if not lines:
        stdout.write("0\n")
        return
    idx = 0
    header = lines[idx].split()
    idx += 1
    part = int(header[1]) if header[0].upper() == "PART" else 2
    n = int(lines[idx])
    idx += 1
    start: list[int] = []
    duration: list[int] = []
    volume: list[int] = []
    for _ in range(n):
        s, d, v = lines[idx].split()
        idx += 1
        start.append(int(s))
        duration.append(int(d))
        volume.append(int(v))
    fn = part1 if part == 1 else part2
    stdout.write(f"{fn(start, duration, volume)}\n")


if __name__ == "__main__":
    main()
