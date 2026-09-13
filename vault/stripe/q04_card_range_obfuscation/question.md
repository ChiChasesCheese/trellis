# q04 · Card Range Obfuscation — fill the gaps in a BIN's brand intervals

## Context
Card numbers are 8–19 digits; the first 6 digits are the **BIN** (bank identification number)
that identifies the issuer. Stripe's card-metadata service answers "which brand is card X?" by
looking up intervals of card numbers inside a BIN, e.g. `4242421500000000–4242426555555555 → VISA`.
Intervals published by issuers leave **gaps**; a fraudster can probe those gaps to discover which
numbers are real. Your job is to *obfuscate* the table: extend the intervals so that the whole
BIN range (`BIN0000000000`…`BIN9999999999`, 16 digits, inclusive endpoints) is covered, then
merge what can be merged, and print the table in a canonical order.

## Input (stdin)
```
PART n                      (optional; n ∈ 1..4 — which rule set to apply; missing → PART 4)
424242                      6-digit BIN
N                           number of intervals (may be 0)
start,end,brand             N lines; start/end are 10-digit OFFSETS after the BIN, inclusive.
```
Blank lines and spaces around separators are ignored. `brand` is any non-empty token and is
reproduced exactly as given (`VISA` and `Visa` are different brands). Intervals may be given in
any order. `start ≤ end` always. Up to 10^5 intervals. Tolerance: a start/end token of 16
digits (≥ 10^10) is treated as an already-full card number.

## Output (stdout)
One line per interval, `start,end,brand`, where start/end are **full 16-digit numbers, zero-padded**
(`BIN × 10^10 + offset`, printed with `%016d`). Sorted by `(start, end, brand)` ascending on the
*final* (extended) values. `N = 0` → print nothing (there is no brand to assign the range to).

## Rules (each part keeps all earlier rules — one program, `PART n` selects how far to go)
Let `LO = BIN·10^10` and `HI = BIN·10^10 + 9999999999` (full numbers).

### Part 1 — extend the outer ends (4 tests)
The interval with the **smallest start** gets `start = LO`; the interval with the **largest end**
gets `end = HI`. Nothing else changes (interior gaps stay). A single interval therefore becomes the
whole BIN range.

### Part 2 — fill interior gaps by extending the LOWER interval upward (4 tests)
Walk the intervals in sorted order. Whenever the next interval starts *after* the highest end seen
so far plus one (`next.start > covered_end + 1`), extend the interval that owns `covered_end`
so that `end = next.start − 1`. Touching intervals (`end + 1 == next.start`) have no gap and are
left alone. Overlapping intervals are not trimmed — they are printed as given (after extension).

### Part 3 — nested / contained intervals (2 tests)
When an interval lies completely inside another (`A.start ≤ B.start` and `B.end ≤ A.end`), only
the **covering** interval `A` may be extended; the contained one keeps its bounds. Concretely:
the interval that is extended to close a gap is the one holding the *maximum end seen so far*,
not the interval printed immediately before the gap. If two intervals share that maximum end,
the one with the smaller start (the one that contains the other) is extended; identical intervals
→ the first in sorted order. Output remains sorted by `(start, end, brand)`, so a contained
interval is printed *after* its covering interval.

### Part 4 — merge adjacent intervals of the same brand (3 tests)
After all extensions, walk the sorted list and merge consecutive intervals whose brand is
identical (exact string match) and that touch or overlap (`next.start ≤ current.end + 1`) into
`[min start, max end]`. Repeat until nothing merges (a single left-to-right pass with a running
"current" interval does it). Different brands never merge, even when touching.

## Worked examples
### Example 1 (Part 1..4 give the same result) — sample 1 from the sources
```
424242
1
1500000000,6555555555,VISA
```
→
```
4242420000000000,4242429999999999,VISA
```

### Example 2 — sample 2 from the sources (touching intervals: no gap)
```
777777
2
1000000000,3999999999,VISA
4000000000,5999999999,MASTERCARD
```
→
```
7777770000000000,7777773999999999,VISA
7777774000000000,7777779999999999,MASTERCARD
```
(Part 1: VISA start → …0000000000, MASTERCARD end → …9999999999; the two touch, so nothing else.)

### Example 3 — interior gaps, unsorted input (PART 2 vs PART 4)
```
PART 2
424242
3
1000000000,1999999999,VISA
5000000000,5999999999,MASTERCARD
3000000000,3999999999,VISA
```
→
```
4242420000000000,4242422999999999,VISA
4242423000000000,4242424999999999,VISA
4242425000000000,4242429999999999,MASTERCARD
```
Same input with `PART 4` → the two touching VISA intervals merge:
```
4242420000000000,4242424999999999,VISA
4242425000000000,4242429999999999,MASTERCARD
```
With `PART 1` the interior gaps stay: `…0000000000,…1999999999,VISA` / `…3000000000,…3999999999,VISA` / `…5000000000,…9999999999,MASTERCARD`.

### Example 4 — nested interval (PART 3)
```
PART 3
424242
3
1000000000,7999999999,VISA
2000000000,2999999999,AMEX
9000000000,9999999999,MASTERCARD
```
→
```
4242420000000000,4242428999999999,VISA
4242422000000000,4242422999999999,AMEX
4242429000000000,4242429999999999,MASTERCARD
```
The gap `8000000000–8999999999` is closed by VISA (it owns the highest end seen, 7999999999),
**not** by AMEX, which is the interval printed right before the gap. AMEX keeps its bounds.

### Example 5 — merge (PART 4)
```
PART 4
555555
4
0000000000,0999999999,MASTERCARD
1000000000,1999999999,MASTERCARD
3000000000,3999999999,VISA
6000000000,6999999999,VISA
```
→
```
5555550000000000,5555552999999999,MASTERCARD
5555553000000000,5555559999999999,VISA
```

## 关联知识点

- [[s01-read-full-spec-first|S01 先读完整份规格，为 Part N+1 而设计]]
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s13-closed-intervals-offbyone|S13 闭区间、补齐空隙、off-by-one 纪律]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s20-self-test-discipline|S20 自测纪律]]
