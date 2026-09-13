"""ps11 Factory Cost — reference solution.

RECONSTRUCTED TRAINING PROBLEM — see problem.md's warning block. Not a real Stripe question.

Four unlock-next-part levels over the same shape (a FACTORIES table + a PENALTIES band table):
  Part 1: build everything, sum the build costs.
  Part 2: add an adjacency proximity penalty between every pair of consecutively built factories.
  Part 3: allow skipping at most one factory to minimize total cost (prefix-sum argmin, see A01
          in skills_matrix.md).
  Part 4: allow skipping up to k factories (DP with reconstruction of the chosen skip set).

Money is integer cents end to end (`parse_money_to_cents` / `fmt_cents`) — no floats anywhere;
there is nothing to round because the input never carries more than 2 decimal digits (a third
digit is a hard format error, not something to round away).
"""

from __future__ import annotations

import sys
from typing import NamedTuple, Optional


class Factory(NamedTuple):
    fid: str
    position: int
    build_cost: int  # cents


class Band(NamedTuple):
    min_dist: int
    max_dist: Optional[int]  # None == the literal 'inf' (open-ended top band)
    penalty: int  # cents

    def contains(self, dist: int) -> bool:
        """Closed interval [min_dist, max_dist] -- both boundaries belong to this band."""
        return self.min_dist <= dist and (self.max_dist is None or dist <= self.max_dist)


# ------------------------------------------------------------------ money


def parse_money_to_cents(raw: str) -> int:
    """'5', '5.0', '5.00', '12.50' -> cents. More than 2 decimal digits is a format error --
    the input never carries sub-cent precision, so there is nothing to round: we reject rather
    than silently truncate or round it away."""
    whole, _, frac = raw.strip().partition(".")
    if len(frac) > 2:
        raise ValueError(f"too many decimal places: {raw!r}")
    return int(whole) * 100 + int(frac.ljust(2, "0"))  # '5.5' -> frac '50', not '05'


def fmt_cents(cents: int) -> str:
    """Two decimals, '$' sign, no thousands separator: 23700 -> '$237.00'."""
    return f"${cents // 100}.{cents % 100:02d}"


# ------------------------------------------------------------------ parsing


def _split_sections(lines: list[str], expect_skip: bool):
    """'FACTORIES', rows..., 'PENALTIES', rows..., ['SKIP', k]
    -> (factory_rows, penalty_rows, k_or_None)."""
    lines = [ln.strip() for ln in lines if ln.strip()]
    if not lines or lines[0] != "FACTORIES":
        raise ValueError("expected a FACTORIES section")
    if "PENALTIES" not in lines:
        raise ValueError("expected a PENALTIES section")
    p_idx = lines.index("PENALTIES")
    factory_rows = lines[1:p_idx]
    rest = lines[p_idx + 1 :]
    if not expect_skip:
        return factory_rows, rest, None
    if "SKIP" not in rest:
        raise ValueError("expected a SKIP section")
    s_idx = rest.index("SKIP")
    penalty_rows = rest[:s_idx]
    k = int(rest[s_idx + 1])
    return factory_rows, penalty_rows, k


def _parse_factories(rows: list[str]) -> list[Factory]:
    out = []
    for row in rows:
        fid, pos, cost = (p.strip() for p in row.split(","))
        out.append(Factory(fid, int(pos), parse_money_to_cents(cost)))
    return out


def _parse_bands(rows: list[str]) -> list[Band]:
    """Bands are untrusted to be in order -- sort by min_dist before use (same discipline as
    ps02's rate tiers)."""
    out = []
    for row in rows:
        mn, mx, pen = (p.strip() for p in row.split(","))
        out.append(Band(int(mn), None if mx == "inf" else int(mx), parse_money_to_cents(pen)))
    out.sort(key=lambda b: b.min_dist)
    return out


def _lookup(bands: list[Band], dist: int) -> Optional[int]:
    """The one band (if any) whose closed interval contains dist. Bands count is tiny (<=20 by
    spec) so a linear scan is simplest and plenty fast; no need for bisect at this scale."""
    for band in bands:
        if band.contains(dist):
            return band.penalty
    return None


def _pair_penalties(factories: list[Factory], bands: list[Band]) -> list[Optional[int]]:
    """One entry per adjacent pair (i, i+1) in corridor order, len == len(factories) - 1.
    None where no band matches that pair's distance."""
    out = []
    for i in range(len(factories) - 1):
        dist = factories[i + 1].position - factories[i].position
        out.append(_lookup(bands, dist))
    return out


# ------------------------------------------------------------------ Part 1 & 2


def part1(lines: list[str]) -> list[str]:
    """Build every factory. TOTAL = sum(build_cost)."""
    factory_rows, _, _ = _split_sections(lines, expect_skip=False)
    factories = _parse_factories(factory_rows)
    total = sum(f.build_cost for f in factories)
    return [f"TOTAL {fmt_cents(total)}"]


def part2(lines: list[str]) -> list[str]:
    """Build every factory, plus one proximity penalty per adjacent pair. A pair whose distance
    matches no band is an error (first such pair, i.e. smallest index, if several)."""
    factory_rows, penalty_rows, _ = _split_sections(lines, expect_skip=False)
    factories = _parse_factories(factory_rows)
    bands = _parse_bands(penalty_rows)
    pairs = _pair_penalties(factories, bands)
    for i, penalty in enumerate(pairs):
        if penalty is None:
            dist = factories[i + 1].position - factories[i].position
            return [f"ERROR no penalty band for distance={dist}"]
    total = sum(f.build_cost for f in factories) + sum(pairs)
    return [f"TOTAL {fmt_cents(total)}"]


# ------------------------------------------------------------------ Part 3 (prefix-sum argmin, A01)


def part3(lines: list[str]) -> list[str]:
    """Skip at most one factory. Every candidate ('skip nothing' + one per factory) is scored in
    O(1) using prefix counts/sums over the n-1 original adjacent-pair penalties, then the whole
    set of valid candidates is argmin-reduced with an explicit tie-break (A01 pattern)."""
    factory_rows, penalty_rows, _ = _split_sections(lines, expect_skip=False)
    factories = _parse_factories(factory_rows)
    bands = _parse_bands(penalty_rows)
    n = len(factories)
    build_sum = sum(f.build_cost for f in factories)

    if n < 2:
        # No adjacent pairs exist either way, and skipping the sole factory (n == 1) would leave
        # zero factories built, which is never a considered configuration.
        return [f"TOTAL {fmt_cents(build_sum)}", "SKIPPED NONE"]

    pairs = _pair_penalties(factories, bands)  # len n - 1, Optional[int]
    prefix_invalid = [0] * n  # prefix_invalid[m] = # of None among pairs[0:m]
    prefix_amount = [0] * n  # prefix_amount[m] = sum(pairs[0:m], treating None as 0)
    for i in range(n - 1):
        prefix_invalid[i + 1] = prefix_invalid[i] + (1 if pairs[i] is None else 0)
        prefix_amount[i + 1] = prefix_amount[i] + (pairs[i] or 0)
    total_invalid = prefix_invalid[n - 1]
    total_amount = prefix_amount[n - 1]

    # candidates: (total_cost, tie_break_rank) -- rank -1 == 'skip nothing' (always wins ties
    # against any 'skip j'); rank j == 'skip factory j' (smaller j wins ties against larger j).
    candidates: list[tuple[int, int, Optional[str]]] = []
    if total_invalid == 0:
        candidates.append((build_sum + total_amount, -1, None))

    for j in range(n):
        removed = [idx for idx in (j - 1, j) if 0 <= idx <= n - 2]
        invalid_removed = sum(1 for idx in removed if pairs[idx] is None)
        if total_invalid - invalid_removed != 0:
            continue  # some OTHER pair (unaffected by skipping j) still has no band -> invalid
        bridge_amount = 0
        if 0 < j < n - 1:
            dist = factories[j + 1].position - factories[j - 1].position
            bridge = _lookup(bands, dist)
            if bridge is None:
                continue
            bridge_amount = bridge
        removed_amount = sum((pairs[idx] or 0) for idx in removed)
        total = build_sum - factories[j].build_cost + (total_amount - removed_amount) + bridge_amount
        candidates.append((total, j, factories[j].fid))

    if not candidates:
        return ["ERROR no valid configuration"]

    total, _rank, fid = min(candidates, key=lambda c: (c[0], c[1]))
    return [f"TOTAL {fmt_cents(total)}", f"SKIPPED {fid if fid is not None else 'NONE'}"]


# ------------------------------------------------------------------ Part 4 (DP + reconstruction)


def part4(lines: list[str]) -> list[str]:
    """Skip up to k factories. dp[i][s] = min cost of a plan whose last built factory is i, having
    skipped s factories among 0..i-1. Reconstructed via explicit back-pointers, following the
    tie-break rules pinned in problem.md (prefer fewer skips per step, then fewer total skips,
    then the largest last-built index)."""
    factory_rows, penalty_rows, k = _split_sections(lines, expect_skip=True)
    factories = _parse_factories(factory_rows)
    bands = _parse_bands(penalty_rows)
    n = len(factories)

    if n == 0:
        return [f"TOTAL {fmt_cents(0)}", "SKIPPED NONE"]

    INF = float("inf")
    dp = [[INF] * (k + 1) for _ in range(n)]
    back: list[list[Optional[int]]] = [
        [None] * (k + 1) for _ in range(n)
    ]  # None sentinel, -1 == "first built"

    for i in range(n):
        s0 = i  # i is the first built factory -> skips exactly the i factories before it
        if s0 <= k:
            dp[i][s0] = factories[i].build_cost
            back[i][s0] = -1
        for j in range(i):
            skipped_between = i - j - 1
            dist = factories[i].position - factories[j].position
            penalty = _lookup(bands, dist)
            if penalty is None:
                continue
            for s_prev in range(k + 1 - skipped_between):
                if dp[j][s_prev] == INF:
                    continue
                s_new = s_prev + skipped_between
                cost = dp[j][s_prev] + factories[i].build_cost + penalty
                cur = dp[i][s_new]
                # tie-break: at equal cost, prefer the LARGER j (fewer skips in this one step).
                if cost < cur or (cost == cur and j > (back[i][s_new] if back[i][s_new] is not None else -1)):
                    dp[i][s_new] = cost
                    back[i][s_new] = j

    # Pick the terminal state: last built index i, skips-so-far s, plus (n - 1 - i) trailing skips.
    best: Optional[tuple[int, int, int]] = None  # (cost, total_skips, -i) for a max-heap-like min compare
    for i in range(n):
        trailing = n - 1 - i
        for s in range(k + 1):
            if dp[i][s] == INF or s + trailing > k:
                continue
            total_skips = s + trailing
            if best is None or (dp[i][s], total_skips, -i) < best:
                best = (dp[i][s], total_skips, -i)
                best_state = (i, s)

    if best is None:
        return [f"ERROR no valid configuration within skip budget k={k}"]

    total_cost = best[0]
    i, s = best_state
    built = set()
    cur_i, cur_s = i, s
    while cur_i != -1:
        built.add(cur_i)
        prev = back[cur_i][cur_s]
        if prev is None:
            raise AssertionError("unreachable dp state during backtrack")
        if prev == -1:
            break
        skipped_between = cur_i - prev - 1
        cur_s -= skipped_between
        cur_i = prev
    skipped_ids = [f.fid for idx, f in enumerate(factories) if idx not in built]
    skipped_str = ",".join(skipped_ids) if skipped_ids else "NONE"
    return [f"TOTAL {fmt_cents(total_cost)}", f"SKIPPED {skipped_str}"]


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
