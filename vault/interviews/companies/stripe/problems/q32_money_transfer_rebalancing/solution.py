"""q32 Money Transfer / Rebalancing — reference solution.

All balances are integer units.  `net = balance - minimum`: net < 0 is a deficit that must be
covered, net > 0 is a surplus that may be used.  Feasible iff sum(balances) >= minimum * n.
"""
from __future__ import annotations

import sys
from typing import NamedTuple


class Account(NamedTuple):
    name: str
    balance: int


class Transfer(NamedTuple):
    src: str
    dst: str
    amount: int

    def __str__(self) -> str:
        return f"from: {self.src}, to: {self.dst}, amount: {self.amount}"


def feasible(accounts: list[Account], minimum: int) -> bool:
    # non-strict: everybody landing exactly on the minimum is fine
    return sum(a.balance for a in accounts) >= minimum * len(accounts)


def _two_pointer(sources: list[list], sinks: list[list], fee: int = 0) -> list[Transfer] | None:
    """sources/sinks: [name, remaining] lists (mutated).  Returns None if a sink stays unfilled."""
    out: list[Transfer] = []
    i = 0
    for sink in sinks:
        while sink[1] > 0:
            if i >= len(sources):
                return None
            src = sources[i]
            usable = src[1] - fee                 # the sender pays the fee on top of the amount
            if usable <= 0:
                i += 1
                continue
            amount = min(usable, sink[1])
            out.append(Transfer(src[0], sink[0], amount))
            src[1] -= amount + fee
            sink[1] -= amount
            if src[1] - fee <= 0:                 # source exhausted (cannot afford another transfer)
                i += 1
    return out


def rebalance_in_order(accounts: list[Account], minimum: int = 100) -> list[Transfer] | None:
    """Part 1: sources and sinks walked in input order."""
    if not feasible(accounts, minimum):
        return None
    sources = [[a.name, a.balance - minimum] for a in accounts if a.balance > minimum]
    sinks = [[a.name, minimum - a.balance] for a in accounts if a.balance < minimum]
    return _two_pointer(sources, sinks)


def rebalance_greedy(accounts: list[Account], minimum: int = 100, fee: int = 0) -> list[Transfer] | None:
    """Largest surplus -> largest deficit (ties by name).  Heuristic for the transfer count."""
    if not feasible(accounts, minimum):
        return None
    sources = sorted(([a.name, a.balance - minimum] for a in accounts if a.balance > minimum), key=lambda s: (-s[1], s[0]))
    sinks = sorted(([a.name, minimum - a.balance] for a in accounts if a.balance < minimum), key=lambda s: (-s[1], s[0]))
    return _two_pointer(sources, sinks, fee)


def min_transfers_exact(accounts: list[Account], minimum: int = 100) -> list[Transfer] | None:
    """Fewest transfers by DFS over deficits with branch-and-bound.  Every transfer either settles the
    deficit or drains the source (an optimal solution with that property always exists)."""
    if not feasible(accounts, minimum):
        return None
    sinks = sorted(((minimum - a.balance, a.name) for a in accounts if a.balance < minimum), reverse=True)
    sources = sorted(((a.balance - minimum, a.name) for a in accounts if a.balance > minimum), reverse=True)
    need = [d for d, _ in sinks]
    rem = [s for s, _ in sources]
    best: list[Transfer] | None = None
    path: list[Transfer] = []

    def dfs(k: int, start: int) -> None:
        nonlocal best
        if k == len(sinks):
            if best is None or len(path) < len(best):
                best = list(path)
            return
        if best is not None and len(path) + (len(sinks) - k) >= len(best):
            return                                   # bound: each open deficit needs >= 1 transfer
        seen = set()
        for j in range(start, len(sources)):
            if rem[j] <= 0 or rem[j] in seen:        # identical remaining surpluses are interchangeable
                continue
            seen.add(rem[j])
            amount = min(rem[j], need[k])
            rem[j] -= amount
            need[k] -= amount
            path.append(Transfer(sources[j][1], sinks[k][1], amount))
            if need[k] == 0:
                dfs(k + 1, 0)
            else:
                dfs(k, j + 1)                        # same deficit, later sources only
            path.pop()
            rem[j] += amount
            need[k] += amount

    dfs(0, 0)
    return best


def apply_transfers(accounts: list[Account], transfers: list[Transfer], minimum: int = 100) -> tuple[list[Account], str]:
    bal = {a.name: a.balance for a in accounts}
    verdict = None
    for t in transfers:
        if t.src not in bal or t.dst not in bal or t.amount <= 0 or t.src == t.dst:
            verdict = "INVALID"
            break
        bal[t.src] -= t.amount
        bal[t.dst] += t.amount
    final = [Account(a.name, bal[a.name]) for a in accounts]
    if verdict is None:
        short = any(b < minimum for b in bal.values())
        if not short:
            verdict = "OK"
        elif feasible(accounts, minimum):
            verdict = "INCOMPLETE"
        else:
            # best effort: impossible overall, and nobody keeps more than the minimum while others are short
            verdict = "NOT_BEST_EFFORT" if any(b > minimum for b in bal.values()) else "BEST_EFFORT"
    return final, verdict


def parse(lines: list[str]) -> tuple[list[Account], list[Transfer], int, int]:
    accounts: list[Account] = []
    transfers: list[Transfer] = []
    minimum, fee = 100, 0
    for raw in lines:
        line = raw.strip().lstrip("-").strip()
        if not line:
            continue
        head = line.split()[0].upper()
        if head == "MIN":
            minimum = int(line.split()[1])
        elif head == "FEE":
            fee = int(line.split()[1])
        elif line.lower().startswith("from:"):
            fields = dict(p.split(":", 1) for p in line.split(","))
            fields = {k.strip().lower(): v.strip() for k, v in fields.items()}
            transfers.append(Transfer(fields["from"], fields["to"], int(fields["amount"])))
        else:
            name, _, amount = line.partition(":")
            accounts.append(Account(name.strip(), int(amount.strip())))
    return accounts, transfers, minimum, fee


def render(transfers: list[Transfer] | None) -> list[str]:
    return ["IMPOSSIBLE"] if transfers is None else [str(t) for t in transfers]


def part1(lines: list[str]) -> list[str]:
    accounts, _, minimum, _ = parse(lines)
    return render(rebalance_in_order(accounts, minimum))


def part2(lines: list[str]) -> list[str]:
    accounts, _, minimum, _ = parse(lines)
    nonzero = sum(1 for a in accounts if a.balance != minimum)
    if nonzero <= 12:
        return render(min_transfers_exact(accounts, minimum))
    return render(rebalance_greedy(accounts, minimum))     # heuristic fallback for large inputs


def part3(lines: list[str]) -> list[str]:
    accounts, transfers, minimum, _ = parse(lines)
    final, verdict = apply_transfers(accounts, transfers, minimum)
    return [f"{a.name}: {a.balance}" for a in final] + [verdict]


def part4(lines: list[str]) -> list[str]:
    accounts, _, minimum, fee = parse(lines)
    transfers = rebalance_greedy(accounts, minimum, fee)
    if transfers is None:
        return ["IMPOSSIBLE"]
    return [str(t) for t in transfers] + [f"FEES: {fee * len(transfers)}"]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 1
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
