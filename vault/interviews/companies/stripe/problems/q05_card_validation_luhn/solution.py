"""q05 Payment Card Validation — reference solution.

Networks are decided by length + prefix; validity additionally needs the Luhn checksum.
Part 3 counts masked completions with a mod-10 DP (per network prefix) instead of enumerating
10^k candidates. Part 4 enumerates the ~150 single-error originals and validates each.
"""
from __future__ import annotations

import sys

# network -> (length, allowed digits per leading position): AMEX 34/37, MC 51-55, VISA 4
NETWORKS: dict[str, tuple[int, tuple[str, ...]]] = {
    "AMEX": (15, ("3", "47")),
    "MASTERCARD": (16, ("5", "12345")),
    "VISA": (16, ("4",)),
}


def luhn_ok(digits: str) -> bool:
    """From the right: double every second digit (starting with the 2nd from the right),
    subtract 9 if > 9, sum all; valid iff sum % 10 == 0."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d = d * 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def network_of(digits: str) -> str | None:
    """Network by length + prefix only (no checksum). None -> UNKNOWN_NETWORK."""
    for name, (length, prefix_sets) in NETWORKS.items():
        if len(digits) == length and all(digits[i] in ok for i, ok in enumerate(prefix_sets)):
            return name
    return None


def classify(digits: str) -> str:
    net = network_of(digits)
    if net is None:                      # length / prefix is checked BEFORE the checksum
        return "UNKNOWN_NETWORK"
    return net if luhn_ok(digits) else "INVALID_CHECKSUM"


def count_completions(masked: str, prefix_sets: tuple[str, ...]) -> int:
    """Number of ways to fill '*' in `masked` so that leading position i uses a digit from
    prefix_sets[i] and the result passes Luhn. DP over positions keeping the running Luhn sum
    mod 10 (10 states) -> O(len * 10 * 10), independent of how many '*' there are."""
    n = len(masked)
    ways = [0] * 10
    ways[0] = 1
    for i, ch in enumerate(masked):
        doubled = (n - 1 - i) % 2 == 1   # parity counted from the right: 2nd, 4th, ... doubled
        allowed = prefix_sets[i] if i < len(prefix_sets) else "0123456789"
        if ch == "*":
            choices = [int(d) for d in allowed]
        elif ch in allowed:
            choices = [int(ch)]
        else:
            return 0                     # fixed digit contradicts the network prefix
        nxt = [0] * 10
        for s in range(10):
            if not ways[s]:
                continue
            for d in choices:
                v = d * 2 - 9 if (doubled and d * 2 > 9) else (d * 2 if doubled else d)
                nxt[(s + v) % 10] += ways[s]
        ways = nxt
    return ways[0]


def masked_counts(masked: str) -> dict[str, int]:
    """network -> count of valid completions (only networks with count > 0)."""
    out: dict[str, int] = {}
    for name, (length, prefix_sets) in NETWORKS.items():
        if len(masked) != length:
            continue
        c = count_completions(masked, prefix_sets)
        if c:
            out[name] = c
    return out


def recover(observed: str) -> list[tuple[str, str]]:
    """All valid originals reachable by undoing exactly one error: one digit changed, or two
    adjacent digits swapped. Deduplicated, ascending numeric order, [(card, network)]."""
    cands: set[str] = set()
    for i, ch in enumerate(observed):
        for d in "0123456789":
            if d != ch:
                cands.add(observed[:i] + d + observed[i + 1:])
    for i in range(len(observed) - 1):
        if observed[i] != observed[i + 1]:       # swapping equal digits is not a change
            cands.add(observed[:i] + observed[i + 1] + observed[i] + observed[i + 2:])
    cands.discard(observed)                      # exactly one error: the original differs
    valid = [(c, network_of(c)) for c in cands]
    return sorted((c, n) for c, n in valid if n is not None and luhn_ok(c))


def part1(lines: list[str]) -> list[str]:
    """16-digit cards starting with 4: VISA / INVALID_CHECKSUM (checksum only)."""
    return ["VISA" if luhn_ok(card.strip()) else "INVALID_CHECKSUM" for card in lines if card.strip()]


def part2(lines: list[str]) -> list[str]:
    return [classify(card.strip()) for card in lines if card.strip()]


def part3(lines: list[str]) -> list[str]:
    out: list[str] = []
    for card in lines:
        counts = masked_counts(card.strip())
        out.extend(f"{name},{counts[name]}" for name in sorted(counts))   # alphabetical by network
    return out


def part4(lines: list[str]) -> list[str]:
    out: list[str] = []
    for card in lines:
        card = card.strip().rstrip("?")
        out.extend(f"{c},{n}" for c, n in recover(card))
    return out


PARTS = {1: part1, 2: part2, 3: part3, 4: part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out: list[str] = []
    if lines and lines[0].upper().startswith("PART"):          # PART n, then one card per line
        part = int(lines[0].split()[1])
        out = PARTS[part](lines[1:])
    else:                                                        # HackerRank form: Q, then 'Pk card'
        if lines and lines[0].isdigit() and len(lines[0]) < 13:  # a count, never a card
            lines = lines[1:]
        for ln in lines:
            if " " in ln:
                tag, card = ln.split()
                part = int(tag[1:])
            else:                                                # bare card: infer the part by shape
                card = ln
                part = 4 if "?" in card else 3 if "*" in card else 2
            out.extend(PARTS[part]([card]))
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
