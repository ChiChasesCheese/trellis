# q08 Store Closing-Time Penalty — report

## Summary
The most-attested Stripe problem (LC 2483 with a Stripe tag): an hourly `Y`/`N` customer log,
a penalty for open-but-empty and closed-but-busy hours, the best closing hour (smallest on tie),
and finally recovering many logs from a noisy `BEGIN … END` text dump. Stripe uses it in the OA
and the phone screen because Part 1 is trivial, Part 2 rewards an O(n) running-sum insight, and
Part 3 is exactly the "ops data is messy" tokenizer-state-machine work they care about.

## Sources & confidence
high — femisowems question4 (verbatim statement + sample I/O, reproduced by the io test),
yingw787 pytest vectors (all 21 reproduced verbatim as parametrized tests), pkafel gist, Hazeera65,
TWINSRIRAM, LC 2585038 phone screen, LC 3950781 Dublin variant, Blind bj5ehdwf, extrabrain/linkjob,
1point3acres 844359.
Conflict resolved: nested `BEGIN`. Hazeera65 notes describe a stack (inner and outer blocks both
reported); femisowems says logs "cannot be nested"; yingw787's vector
`BEGIN BEGIN BEGIN N N BEGIN Y Y END N N END → [2]` implies restart-on-BEGIN. Primary = restart
(brief + executable vector); stack variant documented, not implemented. Reconstructed: the stdin
protocol (`log|closing_time` lines for Part 1, one log per line for Part 2, free text for Part 3),
"non-Y/N token inside a log invalidates it", and `BEGIN END` → 0.

## Approach by part
1. `compute_penalty`: `hours[:t].count("N") + hours[t:].count("Y")` after whitespace tokenizing
   (an unspaced `YYNY` is also expanded per character).
2. `find_best_closing_time`: penalty(0) = #Y; moving the close one hour later adds +1 for `N`,
   −1 for `Y`; keep the first strict minimum → smallest time on ties. O(n), one pass.
3. `get_best_closing_times`: token loop with `current` (None = outside) and `valid`; `BEGIN`
   resets both; `END` emits if open and valid; other tokens append if all-`Y/N`, else invalidate;
   everything outside is ignored.

## Pitfalls hidden tests target
- off-by-one on `t ∈ [0, n]` (open hours are `1..t`), t = 0 and t = n
- `<=` instead of `<` when tracking the minimum (breaks smallest-on-tie); O(n²) on 10^6 hours
- Part 3: nested `BEGIN` (restart, not stack), `END` without `BEGIN`, unfinished trailing log,
  garbage inside vs outside a log, logs spanning / sharing lines, `BEGIN END` → `0`, lowercase tokens

## Complexity & measured cost
All parts O(total tokens). Part 2 on 1 000 000 hours: 0.09 s, 36 MB; Part 3 on 2 000 logs ×
500 hours (~1 000 000 tokens + garbage): 0.23 s (budget 2 s / 256 MB).
Measured: 0.23s, 36 MB

## Test inventory
33 tests — part1: 13 (10 parametrized yingw787 vectors) · part2: 13 (9 parametrized vectors, brute-force
cross-check, perf) · part3: 7 (incl. 1 io, 1 perf); edge 6 · io 1 · perf 2.
`IMPL=starter`: 27 fail / 6 pass (cases whose expected output is empty or 0).

## Skills exercised
S02 tokenizing noisy text · S05 off-by-one discipline · S08 smallest-on-tie · S10 token-stream
state machine · S18 invalid / unfinished input · S19 incremental design (Part 3 reuses Part 2)
