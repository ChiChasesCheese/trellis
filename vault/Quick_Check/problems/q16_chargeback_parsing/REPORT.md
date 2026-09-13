# q16 Chargeback Parsing — report

## Summary
The 2024 University/New-Grad OA: parse card-network chargeback files into merchant-facing dispute
lines, then harden the parser against corrupted rows, then cancel disputes the cardholder withdrew.
It is a pure parse → validate → de-duplicate pipeline; the traps are money formatting per currency
(minor units, zero-decimal JPY), date validation, and the "remove BOTH rows" reversal rule.

## Sources & confidence
medium — leetcode discuss 5832245 (verbatim three-part description, 2024-09-25) and programhelp
2025-08-08 repost. The record layout `network,txn_id,amount,currency,reason,date`, the output line and
the corruption list are reconstructed (marked in problem.md); the withdrawn rule is verbatim.

## Approach by part
1. `parse_row` → `Dispute(NamedTuple)`; `render` = `[NET] id: money CUR - reason (date)`; `fmt_money`
   uses `SYMBOLS` (`$ € £ ¥ ₩`) and `ZERO_DECIMAL = {jpy, krw}`; other currencies `x.xx` without symbol.
2. `parse_row` returns `None` on: field count ≠ 6, `int(amount)` failure or negative, `strptime` failure,
   unknown network, empty id/currency/reason. `parse_all` counts them; `SKIPPED: n` always printed.
3. `withdrawn = {(network, txn_id) for valid rows with reason == 'withdrawn'}`; print valid rows not in
   that set, in input order. Order-independent, so withdrawn-first, double-withdrawn and lone-withdrawn
   all fall out of the same set membership.

## Pitfalls hidden tests target
- `2500` printed as `$2500.00`, or JPY printed with decimals; `5` → `$0.05`; unknown currency symbol
- `25.00` accepted via `float`; `2024-02-30` accepted by hand-rolled checks; `2024-2-3` parses (strptime)
  and must be re-printed zero-padded
- `SKIPPED: 0` missing; blank lines counted as corrupted
- Part 3: only removing the withdrawn row (not the original), or only handling "withdrawn after";
  cancelling across networks; a *corrupted* withdrawal cancelling; counting withdrawn rows as skipped
- NB (tooling): `@dataclass` fails under the repo's `spec_from_file_location` loader
  (`sys.modules[cls.__module__]` missing) — use `NamedTuple` / plain classes in solutions.

## Complexity & measured cost
O(n) time and memory. Measured: 0.75s, 148 MB (200k rows, 15% withdrawn, 5% corrupted, 128k output
lines; in-pytest 0.98 s; budget 2 s / 256 MB). Memory is dominated by holding all rows + output.

## Test inventory
18 tests — part1: 6 · part2: 5 · part3: 7; edge 10 · fmt 2 · io 2 · perf 1.

## Skills exercised
S02 delimited parsing with malformed rows · S06 minor-unit money / zero-decimal · S09 exact formatting ·
S11 reversal de-duplication · S12 date validation · S18 validation paths · S24 dispute vocabulary
