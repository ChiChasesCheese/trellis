"""pc21 Accumulator Interpreter -- reference solution.

Part1 is TrueInterview's "String-Command Calculator": a single accumulator starting at 0,
commands ADD/SUB/MULT/DIV n. DIV is integer division TRUNCATED TOWARD ZERO (not Python's floor
`//`, which rounds toward -inf -- they differ whenever the signs of the operands differ), and
division by zero raises ValueError (reconstructed choice, stated here).

Part2 is TrueInterview's "SnowCal": a single global variable X starting at 0, instructions
ADD n / MUL n / FUN name ... END (declares a function -- its body is NOT executed at the
declaration site, only registered) / INV name (invokes a previously-declared function's body in
place, mutating the same global X). Functions may INV other functions; both an INV of an
undefined name and a call cycle (direct or indirect self-recursion) raise ValueError -- a cycle
is detected via the set of function names currently "in progress" on the INV call chain, so it
is caught immediately rather than by actually looping forever.

Part3 (reconstructed) is the natural "now count gets huge" follow-up: a REPEAT count name
instruction that invokes a function `count` times (count can be up to ~10**15), with all
arithmetic mod 1_000_000_007. Naively looping `count` times would be far too slow, so instead
every function's net effect on X is represented once as an AFFINE MAP x -> a*x + b (ADD n is
(1, n), MUL n is (n, 0), and composing two affine maps -- including calling another already-
memoised function -- is again affine); repeating an affine map k times has a closed form
(a**k, b * (a**k - 1) / (a - 1), using a modular inverse since MOD is prime -- or b*k when
a == 1 mod MOD), computed in O(log k) via fast modular exponentiation. So REPEAT is O(log count)
regardless of how large count is, and a function's affine map is computed once and memoised.
"""

from __future__ import annotations

import sys

MOD = 1_000_000_007


def _check_int_tokens(parts: list[str], stmt: str) -> None:
    if len(parts) != 2:
        raise ValueError(f"malformed instruction {stmt!r}")


def _trunc_div(a: int, b: int) -> int:
    """Integer division truncated TOWARD ZERO (unlike Python's `//`, which floors)."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


# --------------------------------------------------------------------------- Part 1
def run_calculator(commands: list[str]) -> int:
    """Accumulator starts at 0. ADD/SUB/MULT/DIV n, applied in order. DIV truncates toward
    zero; dividing by zero raises ValueError. Unknown command -> ValueError."""
    acc = 0
    for stmt in commands:
        parts = stmt.split()
        if not parts:
            raise ValueError("empty instruction")
        op = parts[0]
        if op not in ("ADD", "SUB", "MULT", "DIV"):
            raise ValueError(f"unknown command {stmt!r}")
        _check_int_tokens(parts, stmt)
        n = int(parts[1])
        if op == "ADD":
            acc += n
        elif op == "SUB":
            acc -= n
        elif op == "MULT":
            acc *= n
        else:  # DIV
            if n == 0:
                raise ValueError("division by zero")
            acc = _trunc_div(acc, n)
    return acc


# --------------------------------------------------------------------------- Part 2
def _split_functions(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    """Registers every top-level 'FUN name ... END' block into a dict (functions cannot be
    nested -- a FUN body holds only ADD/MUL/INV lines) and returns the remaining top-level
    statements in order, with the FUN...END blocks removed (declaring a function does not run
    it)."""
    funcs: dict[str, list[str]] = {}
    top_level: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        parts = lines[i].split()
        if parts[0] == "FUN":
            if len(parts) != 2:
                raise ValueError(f"malformed FUN header {lines[i]!r}")
            name = parts[1]
            body: list[str] = []
            i += 1
            while i < n and lines[i] != "END":
                body.append(lines[i])
                i += 1
            if i == n:
                raise ValueError(f"FUN {name!r} missing matching END")
            funcs[name] = body
            i += 1  # skip END
        else:
            top_level.append(lines[i])
            i += 1
    return top_level, funcs


def _exec_snowcal_stmt(stmt: str, x: int, funcs: dict[str, list[str]], chain: frozenset) -> int:
    parts = stmt.split()
    op = parts[0]
    if op == "ADD":
        _check_int_tokens(parts, stmt)
        return x + int(parts[1])
    if op == "MUL":
        _check_int_tokens(parts, stmt)
        return x * int(parts[1])
    if op == "INV":
        if len(parts) != 2:
            raise ValueError(f"malformed instruction {stmt!r}")
        name = parts[1]
        if name not in funcs:
            raise ValueError(f"call to undefined function {name!r}")
        if name in chain:
            raise ValueError(f"infinite recursion detected: {name!r} calls itself (directly or indirectly)")
        for inner in funcs[name]:
            x = _exec_snowcal_stmt(inner, x, funcs, chain | {name})
        return x
    raise ValueError(f"unknown instruction {stmt!r}")


def run_snowcal(lines: list[str]) -> int:
    """X starts at 0. ValueError for INV of an undefined function or for a call cycle."""
    top_level, funcs = _split_functions(lines)
    x = 0
    for stmt in top_level:
        x = _exec_snowcal_stmt(stmt, x, funcs, frozenset())
    return x


# --------------------------------------------------------------------------- Part 3
def _compose(a1: int, b1: int, a2: int, b2: int) -> tuple[int, int]:
    """Affine map2 applied AFTER map1: result(x) = a2*(a1*x + b1) + b2, mod MOD."""
    return (a2 * a1) % MOD, (a2 * b1 + b2) % MOD


def _affine_power(a: int, b: int, k: int) -> tuple[int, int]:
    """The affine map x -> a*x + b, composed with itself k times, mod MOD, in O(log k)."""
    if k == 0:
        return 1, 0
    a %= MOD
    if a == 1:
        return 1, (b * (k % MOD)) % MOD
    ak = pow(a, k, MOD)
    inv_a_minus_1 = pow(a - 1, MOD - 2, MOD)  # MOD is prime -> Fermat's little theorem
    total_b = (b % MOD) * ((ak - 1) % MOD) % MOD * inv_a_minus_1 % MOD
    return ak, total_b


def _affine_of_instructions(
    instructions: list[str],
    funcs: dict[str, list[str]],
    memo: dict[str, tuple[int, int]],
    chain: frozenset,
) -> tuple[int, int]:
    a, b = 1, 0
    for stmt in instructions:
        parts = stmt.split()
        op = parts[0]
        if op == "ADD":
            a, b = _compose(a, b, 1, int(parts[1]) % MOD)
        elif op == "MUL":
            a, b = _compose(a, b, int(parts[1]) % MOD, 0)
        elif op == "INV":
            fa, fb = _affine_of_function(parts[1], funcs, memo, chain)
            a, b = _compose(a, b, fa, fb)
        elif op == "REPEAT":
            if len(parts) != 3:
                raise ValueError(f"malformed instruction {stmt!r}")
            count, name = int(parts[1]), parts[2]
            if count < 0:
                raise ValueError("REPEAT count must be >= 0")
            fa, fb = _affine_of_function(name, funcs, memo, chain)
            ra, rb = _affine_power(fa, fb, count)
            a, b = _compose(a, b, ra, rb)
        else:
            raise ValueError(f"unknown instruction {stmt!r}")
    return a, b


def _affine_of_function(
    name: str,
    funcs: dict[str, list[str]],
    memo: dict[str, tuple[int, int]],
    chain: frozenset,
) -> tuple[int, int]:
    if name in memo:
        return memo[name]
    if name not in funcs:
        raise ValueError(f"call to undefined function {name!r}")
    if name in chain:
        raise ValueError(f"infinite recursion detected: {name!r} calls itself (directly or indirectly)")
    result = _affine_of_instructions(funcs[name], funcs, memo, chain | {name})
    memo[name] = result
    return result


def run_snowcal_mod(lines: list[str]) -> int:
    """Same language as Part2 plus 'REPEAT count name' (invoke `name` count times, count up to
    ~10**15), all arithmetic mod 1_000_000_007. O(program length * log(max count)) regardless of
    how large the counts are, via memoised per-function affine maps."""
    top_level, funcs = _split_functions(lines)
    memo: dict[str, tuple[int, int]] = {}
    a, b = _affine_of_instructions(top_level, funcs, memo, frozenset())
    return (a * 0 + b) % MOD  # X starts at 0


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """each line is one program (commands separated by ';') -> the final accumulator."""
    return [str(run_calculator(line.split(";"))) for line in lines]


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'N' (number of instructions in the one program that follows), then N
    instruction lines -> a single line with the final X."""
    n = int(lines[0])
    program = lines[1 : 1 + n]
    return [str(run_snowcal(program))]


def part3(lines: list[str]) -> list[str]:
    n = int(lines[0])
    program = lines[1 : 1 + n]
    return [str(run_snowcal_mod(program))]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
