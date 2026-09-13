# qA07 · LC 56 Merge Intervals + LC 1288 Remove Covered Intervals — merge, covered, brand gap-fill, inclusive integers

LC 56 · *Merge Intervals* · Medium · https://leetcode.com/problems/merge-intervals
LC 1288 · *Remove Covered Intervals* · Medium · https://leetcode.com/problems/remove-covered-intervals

## The problems (restated)
* **LC 56** — given `intervals = [[start, end], ...]` (closed, `start ≤ end`, any order), merge every
  pair that overlaps (sharing even a single point: `[1,4]` and `[4,5]` → `[1,5]`) and return the
  disjoint intervals sorted by start. Limits: `1 ≤ n ≤ 10^4`, `0 ≤ start ≤ end ≤ 10^4`.
* **LC 1288** — given distinct intervals `[l, r]` with `l < r`, remove every interval that is
  **covered** by another (`[a,b]` is covered by `[c,d]` iff `c ≤ a` and `b ≤ d`); return how many
  remain. Limits: `1 ≤ n ≤ 1000`, `0 ≤ l < r ≤ 10^5`.

## Context
Stripe's card-metadata API returns BIN ranges as brand-labelled intervals (q04 Card Range
Obfuscation: extend to the range edges, fill interior gaps by extending the lower interval, only the
covering interval grows when ranges nest, merge touching same-brand ranges). Deployment windows (q29)
subtract freeze intervals from allowed ones. Both bespoke problems are LC 56 + LC 1288 with inclusive
integer endpoints and labels, so the tag pair is the warm-up for them.

## Input (stdin)
```
PART n              # 1..4
start end           # Parts 1, 2, 4: one interval per line
```
Part 3:
```
PART 3
lo hi               # the full range to cover (inclusive integers)
start end label     # one labelled interval per line
```

## Output
* Parts 1 and 4: merged intervals, `start end` per line, sorted by start.
* Part 2: the count on the first line, then the remaining intervals `start end` sorted by start.
* Part 3: `start end label` per line, sorted by `(start, end, label)`.

## Rules
### Part 1 — LC 56  `merge(intervals) -> list[list[int]]`
Sort by `(start, end)`; keep a running interval; the next one merges iff `next.start ≤ cur.end`
(touching endpoints merge, real-number semantics); merged `end = max(ends)`. Empty input → `[]`.

### Part 2 — LC 1288  `remove_covered_intervals(intervals) -> int`, `uncovered(intervals) -> list[list[int]]`
Sort by `(start asc, end desc)` and scan with `max_end`: an interval survives iff `end > max_end`
(with that sort order, anything with `end ≤ max_end` starts at or after a longer interval's start, so
it is covered). Equal intervals: LC guarantees uniqueness; here duplicates count as covering each
other, so only one copy survives. `uncovered` returns the survivors sorted by start.

### Part 3 — brand gap-fill over a full range (q04 link)  `fill_gaps(labeled, lo, hi) -> list[Labeled]`
`Labeled(start, end, label)` NamedTuples with **inclusive integer** endpoints, all inside `[lo, hi]`.
Apply q04's rules in order: (1) the interval with the smallest start gets `start = lo`, the one with
the largest end gets `end = hi` (ties on the largest end → the one with the smaller start, i.e. the
covering one); (2) walk in `(start, end, label)` order tracking `covered_end` and its holder (max end
seen; ties → smaller start, then first); when `next.start > covered_end + 1` extend the holder to
`next.start − 1`; nested intervals keep their own bounds (only the holder grows); (3) merge
**consecutive** entries of the sorted list with an identical label that touch or overlap
(`next.start ≤ cur.end + 1`) into `[min start, max end]`. Return sorted by `(start, end, label)`.
Empty input → `[]`.

### Part 4 — inclusive integer endpoints  `merge_inclusive(intervals) -> list[list[int]]`
LC 56 for integer ranges: `[1,2]` and `[3,4]` are adjacent integers and merge into `[1,4]`;
`[1,2]` and `[4,5]` do not (3 is uncovered). Condition `next.start ≤ cur.end + 1`.

## Worked examples
```
LC 56 ex1   [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
LC 56 ex2   [[1,4],[4,5]] -> [[1,5]]
LC 1288 ex1 [[1,4],[3,6],[2,8]] -> 2   (uncovered: [[1,4],[2,8]])
LC 1288 ex2 [[1,4],[2,3]] -> 1         (uncovered: [[1,4]])
Part 3      lo=0 hi=99, [(10,20,VISA),(30,40,MC),(35,38,AMEX),(50,60,MC),(61,70,MC)]
            step 1: (0,20,VISA) ; (61,99,MC)
            step 2: gap 21..29 -> VISA grows to (0,29) ; AMEX nested in MC (holder of 40 = MC) ;
                    gap 41..49 -> (30,49,MC) ; 50 touches 49 ; 61 touches 60
            step 3: (50,60,MC)+(61,99,MC) -> (50,99,MC) ; (30,49,MC) and (50,99,MC) are NOT consecutive
                    in sorted order (AMEX sits between them) so they stay separate
            -> [(0,29,VISA),(30,49,MC),(35,38,AMEX),(50,99,MC)]
            lo=0 hi=9, [(3,4,X)] -> [(0,9,X)]
Part 4      [[1,2],[3,4]] -> [[1,4]] ; [[1,2],[4,5]] -> [[1,2],[4,5]] ; LC 56 ex1 -> same as Part 1
```
stdin `PART 1` + `1 3 / 2 6 / 8 10 / 15 18` → `1 6`, `8 10`, `15 18`.

## 关联知识点

- [[a09-interval-merge-coverage|A09 区间合并 / 被覆盖区间]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s13-closed-intervals-offbyone|S13 闭区间、补齐空隙、off-by-one 纪律]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
