"""pc01 Grouped Aggregation -- reference solution.

The interview prompt ("given a dataframe or csv with millions of records, group by a common
identifier and find aggregated sums... solved by chunking and re-aggregating") is a streaming /
external-aggregation problem, not a pandas problem: the point is that a single Python process
cannot hold "millions of records" comfortably as one DataFrame, so the candidate is expected to
(a) accumulate with a dict in one pass when it *does* fit, then (b) split into bounded chunks,
aggregate each chunk independently and merge the partial results -- which is correct because
sum/count/max are all associative, so partial dicts merge the same way regardless of chunk size
or how the chunks were scheduled (sequentially or across worker threads/processes).

Part1 is the single-pass dict accumulator using the `csv` module (streaming: never materialises
more than the current row plus the running totals).
Part2 splits the same rows into `chunk_size`-row chunks, aggregates each chunk with Part1's
function, and merges the partial dicts; `workers > 1` fans the per-chunk aggregation out over a
ThreadPoolExecutor. Merge order does not matter (dict addition is commutative), so the result is
identical for workers=1 and workers=N -- that determinism is the thing hidden tests check.
Part3 (reconstructed) generalises to a composite (id, category) key and three aggregates at once
(sum, count, max) in the same single pass.
"""
from __future__ import annotations

import csv
import sys
from concurrent.futures import ThreadPoolExecutor
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Iterable, Iterator, Sequence

TWO_PLACES = Decimal("0.01")
ZERO = Decimal("0.00")


def _to_amount(raw: str) -> Decimal:
    """Parse a decimal string and round to 2 places, half-up (bankers' rounding is not used --
    this is a sum of already-2dp money amounts, so ROUND_HALF_UP only ever fires on malformed
    input with more than 2 decimal places, which is deliberately still accepted)."""
    try:
        value = Decimal(raw.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError(f"invalid amount {raw!r}") from None
    return value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def _parse_row(fields: list[str]) -> tuple[str, Decimal]:
    if len(fields) != 2:
        raise ValueError(f"expected 2 fields 'id,amount', got {fields!r}")
    key = fields[0].strip()
    if not key:
        raise ValueError("id must not be empty")
    return key, _to_amount(fields[1])


def iter_rows(lines: Iterable[str]) -> Iterator[tuple[str, Decimal]]:
    """Streaming parse of 'id,amount' rows via the csv module. `lines` is walked once; nothing
    beyond the current row is held in memory here."""
    reader = csv.reader(ln for ln in lines if ln.strip() != "")
    for fields in reader:
        yield _parse_row(fields)


# --------------------------------------------------------------------------- Part 1
def group_sum_streaming(lines: Iterable[str]) -> dict[str, Decimal]:
    """One pass, one dict, no other container that grows with the row count."""
    totals: dict[str, Decimal] = {}
    for key, amount in iter_rows(lines):
        totals[key] = totals.get(key, ZERO) + amount
    return totals


# --------------------------------------------------------------------------- Part 2
def _merge_totals(a: dict[str, Decimal], b: dict[str, Decimal]) -> dict[str, Decimal]:
    out = dict(a)
    for key, amount in b.items():
        out[key] = out.get(key, ZERO) + amount
    return out


def chunked_group_sum(lines: Sequence[str], chunk_size: int, workers: int = 1) -> dict[str, Decimal]:
    """Split the (already-materialised) rows into `chunk_size`-row chunks, aggregate each chunk
    with `group_sum_streaming`, then merge the partial dicts. `workers > 1` runs the per-chunk
    aggregation on a ThreadPoolExecutor -- CPython's GIL means this is a concurrency *pattern*
    exercise, not a real speed-up for this CPU-bound loop; a real multi-million-row job would use
    ProcessPoolExecutor instead so each worker gets its own interpreter, at the cost of pickling
    each chunk across the process boundary. Either way the merge is identical because dict
    addition is commutative, so results never depend on chunk_size or worker count."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if workers <= 0:
        raise ValueError("workers must be positive")
    rows = [ln for ln in lines if ln.strip() != ""]
    chunks = [rows[i : i + chunk_size] for i in range(0, len(rows), chunk_size)]
    if not chunks:
        return {}
    if workers == 1:
        partials = [group_sum_streaming(chunk) for chunk in chunks]
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            partials = list(pool.map(group_sum_streaming, chunks))
    totals: dict[str, Decimal] = {}
    for partial in partials:
        totals = _merge_totals(totals, partial)
    return totals


# --------------------------------------------------------------------------- Part 3 (reconstructed)
def multi_key_aggregate(lines: Iterable[str]) -> dict[tuple[str, str], dict[str, object]]:
    """Rows 'id,category,amount' -> group by (id, category); per group: sum, count, max, all in
    one pass over the input (same streaming shape as Part1, just a wider accumulator per key)."""
    groups: dict[tuple[str, str], dict[str, object]] = {}
    reader = csv.reader(ln for ln in lines if ln.strip() != "")
    for fields in reader:
        if len(fields) != 3:
            raise ValueError(f"expected 3 fields 'id,category,amount', got {fields!r}")
        key_id, category = fields[0].strip(), fields[1].strip()
        if not key_id or not category:
            raise ValueError("id and category must not be empty")
        amount = _to_amount(fields[2])
        group = groups.setdefault((key_id, category), {"sum": ZERO, "count": 0, "max": None})
        group["sum"] += amount
        group["count"] += 1
        if group["max"] is None or amount > group["max"]:
            group["max"] = amount
    return groups


# --------------------------------------------------------------------------- line-driven wrappers
def _fmt_amount(value: Decimal) -> str:
    return f"{value:.2f}"


def part1(lines: list[str]) -> list[str]:
    """rows: 'id,amount' (no header, one per line). Output: 'id,total' sorted by id, ascending."""
    totals = group_sum_streaming(lines)
    return [f"{key},{_fmt_amount(total)}" for key, total in sorted(totals.items())]


def part2(lines: list[str]) -> list[str]:
    """lines[0] = 'CHUNK_SIZE <n>', then rows 'id,amount'. Output: same shape as part1."""
    if not lines:
        raise ValueError("missing 'CHUNK_SIZE <n>' header line")
    header = lines[0].split()
    if len(header) != 2 or header[0] != "CHUNK_SIZE":
        raise ValueError("first line must be 'CHUNK_SIZE <n>'")
    chunk_size = int(header[1])
    totals = chunked_group_sum(lines[1:], chunk_size)
    return [f"{key},{_fmt_amount(total)}" for key, total in sorted(totals.items())]


def part3(lines: list[str]) -> list[str]:
    """rows: 'id,category,amount'. Output: 'id,category,sum,count,max' sorted by (id, category)."""
    groups = multi_key_aggregate(lines)
    out = []
    for (key_id, category), agg in sorted(groups.items()):
        out.append(
            f"{key_id},{category},{_fmt_amount(agg['sum'])},{agg['count']},{_fmt_amount(agg['max'])}"
        )
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
