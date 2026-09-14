"""q21 Currency Conversion — reference solution.

Graph: currency -> {neighbour: rate}. Direct quotes are edges; the inverse (1/rate) of a quote is
added only when the opposite ordered pair is not quoted directly. Part 3's "best" rate is the
maximum product over SIMPLE paths (cycles ignored), found by DFS — currency graphs are tiny.
Part 4 recomputes the product along the best path in Decimal and rounds half-up to cents.
"""
from __future__ import annotations

import sys
from collections import deque
from decimal import ROUND_HALF_UP, Decimal

Rates = dict[tuple[str, str], float]


def parse_rates(s: str) -> Rates:
    rates: Rates = {}
    for chunk in s.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        a, b, r = (p.strip() for p in chunk.split(":"))
        rate = float(r)                      # non-numeric -> ValueError
        if rate <= 0:                        # rule: a rate of 0 (or negative) is invalid
            raise ValueError(f"invalid rate {r!r} for {a}:{b}")
        rates[(a, b)] = rate                 # rule: duplicate ordered pair -> last quote wins
    return rates


def fmt_rate(x: float) -> str:
    # exact rule: 6 decimals, then strip trailing zeros and a trailing dot
    return f"{x:.6f}".rstrip("0").rstrip(".") or "0"


def convert(rates: Rates, src: str, dst: str) -> float | None:
    if src == dst:
        return 1.0                           # identity, even for an unknown currency
    return rates.get((src, dst))


def convert_with_inverse(rates: Rates, src: str, dst: str) -> float | None:
    direct = convert(rates, src, dst)
    if direct is not None:
        return direct                        # direct quote beats the inverse of the opposite quote
    back = rates.get((dst, src))
    return None if back is None else 1.0 / back


def adjacency(rates: Rates) -> dict[str, dict[str, float]]:
    """Insertion-ordered adjacency: direct edges first, inverses only where no direct quote."""
    adj: dict[str, dict[str, float]] = {}
    for (a, b), r in rates.items():
        adj.setdefault(a, {})[b] = r
        adj.setdefault(b, {})
    for (a, b), r in rates.items():
        adj[b].setdefault(a, 1.0 / r)
    return adj


def find_path(rates: Rates, src: str, dst: str) -> list[str] | None:
    if src == dst:
        return [src]
    adj = adjacency(rates)
    if src not in adj or dst not in adj:
        return None
    prev: dict[str, str | None] = {src: None}
    queue = deque([src])
    while queue:
        cur = queue.popleft()
        for nxt in adj[cur]:                 # neighbour order = first appearance in the rate string
            if nxt in prev:
                continue
            prev[nxt] = cur
            if nxt == dst:
                path = [dst]
                while prev[path[-1]] is not None:
                    path.append(prev[path[-1]])  # type: ignore[arg-type]
                return path[::-1]
            queue.append(nxt)
    return None


def best_conversion(rates: Rates, src: str, dst: str) -> tuple[float, list[str]] | None:
    if src == dst:
        return 1.0, [src]
    adj = adjacency(rates)
    if src not in adj or dst not in adj:
        return None
    best: tuple[float, list[str]] | None = None
    path = [src]
    on_path = {src}

    def dfs(cur: str, product: float) -> None:
        nonlocal best
        if cur == dst:
            # tie-break: higher product, then fewer hops, then lexicographically smaller path
            cand = (product, list(path))
            if best is None or (product, -len(path)) > (best[0], -len(best[1])) or \
                    ((product, len(path)) == (best[0], len(best[1])) and path < best[1]):
                best = cand
            return
        for nxt, r in adj[cur].items():
            if nxt in on_path:
                continue                     # simple paths only: cycles are ignored
            on_path.add(nxt)
            path.append(nxt)
            dfs(nxt, product * r)
            path.pop()
            on_path.discard(nxt)

    dfs(src, 1.0)
    return best


def convert_payouts(rates: Rates, payouts: list[str]) -> list[str]:
    cache: dict[tuple[str, str], Decimal | None] = {}
    out: list[str] = []
    for raw in payouts:
        amount, src, dst = (p.strip() for p in raw.split(","))
        key = (src, dst)
        if key not in cache:
            res = best_conversion(rates, src, dst)
            if res is None:
                cache[key] = None
            else:
                prod = Decimal(1)
                for a, b in zip(res[1], res[1][1:]):
                    # exact product along the path: direct quote, else 1 / opposite quote
                    prod *= Decimal(repr(rates[(a, b)])) if (a, b) in rates else Decimal(1) / Decimal(repr(rates[(b, a)]))
                cache[key] = prod
        prod = cache[key]
        if prod is None:
            out.append(f"{amount} {src} -> {dst} = N/A")
        else:
            # rounding rule: half-up to the cent
            val = (Decimal(amount) * prod).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            out.append(f"{amount} {src} -> {dst} = {val}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    rates = parse_rates(lines[1]) if len(lines) > 1 else {}
    queries = lines[2:]
    out: list[str] = []
    if part == 4:
        out = convert_payouts(rates, queries)
    else:
        for q in queries:
            src, dst = q.split()
            if part == 1:
                r = convert(rates, src, dst)
                out.append("N/A" if r is None else fmt_rate(r))
            elif part == 2:
                r = convert_with_inverse(rates, src, dst)
                out.append("N/A" if r is None else fmt_rate(r))
            else:
                res = best_conversion(rates, src, dst)
                out.append("N/A" if res is None else f"{fmt_rate(res[0])} {'->'.join(res[1])}")
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
