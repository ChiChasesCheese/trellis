# q41 · Observability Metrics — event stream → windowed aggregation → alerting with hysteresis

**Sources（来源）：** interviewdb.io 收录了一道裸标题「Observability」的 Stripe OA 题
（Coding，2026-08 被发现更新），但正文区域是纯前端占位符（"Loading practice workspace…" /
"No questions are available yet"），WebFetch 多次抓取均拿不到规则、输入输出格式或函数签名——见
`catalog/discovery/2026-09/C_batchA.md` `## C1`。旁证：PracHub 上有一道 onsite 系统设计题
《Design a Count-Metrics Monitoring Platform》，主题（指标/计数/监控平台）高度相关，但它是**系统
设计题**而非编码题，且题面本身也未获取，**只能当主题旁证，不能当题面**用。

**Confidence（置信度）：极低** — 除了"这道 OA 题的标题叫 Observability，主题大概率是指标/日志/
告警"之外，没有任何规则文本。本题**完全自拟**，只保证覆盖"可观测性"这个领域应该考的知识点
（事件流解析、时间窗聚合、告警阈值语义、乱序/迟到事件处理）。

> ⚠️ **重建题（非真题）**：本题面是根据 interviewdb.io 上「Observability」这个**裸标题**（2026-08
> 报道，正文从未公开）**自拟**的训练题；PracHub 的《Design a Count-Metrics Monitoring Platform》
> 只是同主题的旁证，不是这道题的来源。
> 真实题面从未公开——规则、输入格式、输出格式、part 划分**全部是本仓库编的**。
> 练它是为了覆盖 **S02（行式解析）、S12（时间分桶）、S05（阈值语义）、S10（事件流与状态翻转）、
> S16（滑动窗口）、S08（确定性排序）、S09（字节级输出格式）**，**不要把这里的输出格式当成真题
> 格式**去背。

## Context
Stripe's internal metrics pipeline ingests a stream of raw metric events (`name`, `labels`,
`value`, `timestamp`) from every service, buckets them into time windows, and evaluates alerting
rules against the windowed aggregates. A rule shouldn't fire on a single noisy window (flapping),
and shouldn't clear the instant things look okay for one window either — real alerting debounces
both directions. Real event streams also arrive slightly out of order and sometimes very late
(a retried batch, a delayed agent) — a production pipeline has to decide how much lateness to
tolerate before it closes the books on an old window.

## Input (stdin)
```
PART n
WINDOW <size> <step>          (Part 2, 3, 4 only)
RULES                          (Part 3, 4 only)
<rule row>
...
LATENESS <L>                   (Part 4 only)
EVENTS
<event row>
<event row>
...
```
Sections are cumulative in that exact order; a given `PART n` only includes the sections listed
for it above (Part 1 is just `EVENTS`; Part 2 adds `WINDOW`; Part 3 adds `RULES`; Part 4 adds
`LATENESS`). Marker lines are literal and case-sensitive. Blank lines are ignored; optional
spaces around commas are tolerated.

* **`WINDOW <size> <step>`** — both positive integers, seconds, `1 <= step <= size`. Window `k`
  (`k = 0, 1, 2, ...`) covers `[k*step, k*step + size)`. `step == size` is a plain **tumbling**
  (non-overlapping) window; `step < size` is a **sliding** window (each event may fall inside
  more than one window — this is the intended `S16` sliding-window case, not an error).
* **Rule row** (`RULES` section, Part 3/4): `metric_name,labels,stat,op,threshold,trigger_n,clear_n`
  — an 8th field `value_threshold` is **required when, and only when,** `stat` is `rate`.
  Rule rows are trusted configuration (not stream data): a malformed rule row is a fatal
  `ValueError`, not a skip-and-count situation like a malformed event row.
  - `stat` ∈ `{count, avg, rate}` — evaluated over window `k`'s matching events (see below).
    `count` is a raw integer volume check; `rate` is a **ratio** (0.0-1.0) of how many of the
    window's events exceed `value_threshold`, out of the window's total matching events —
    deliberately the "count vs ratio" pair `S05` targets. `avg` is the mean `value` over the
    window's matching events (`0.0` when the window has zero matching events, same as `rate`
    when its denominator is zero — division-by-zero is a defined `0.0`, never a crash).
  - `op` ∈ `{gt, gte, lt, lte}` — `gt`/`lt` are **strict**, `gte`/`lte` are **non-strict**; this
    is the exact boundary `S05` targets (`stat == threshold` behaves differently under `gt` vs
    `gte`).
  - `threshold` (and `value_threshold` when present): a plain decimal string, parsed as a float.
  - `trigger_n`, `clear_n`: positive integers (`>= 1`) — see the hysteresis rule below.
* **`LATENESS <L>`** — a single non-negative integer, Part 4 only: how many windows of lateness
  (measured against `step`, see Part 4) are tolerated before an event is dropped as too late.
* **Event row** (`EVENTS` section, all parts): `timestamp,metric_name,labels,value`
  - `timestamp`: non-negative integer, seconds.
  - `metric_name`: non-empty token, no commas.
  - `labels`: either the literal token `-` (no labels) or `key1=val1;key2=val2;...` (`;`-joined
    `key=value` pairs, keys non-empty and unique within the row, **any order** — canonicalize by
    sorting on key before using it as part of a grouping identity; two rows with the same pairs
    in a different order belong to the **same** series).
  - `value`: a plain decimal string, parsed as a float (no currency/units, this isn't money —
    there is no minor-unit rounding rule here, only the output-formatting rule below).
  - A row is **malformed** or a **format error** if it doesn't have exactly 4 comma-separated
    fields, `timestamp` isn't a valid non-negative integer, `value` doesn't parse as a float, or
    `labels` isn't `-` or a well-formed `key=value;...` list. A malformed row is **skipped** (not
    counted in any aggregation) and tallied — this is the intended `S02` graded case, not a
    crash.
  - Up to 10^5 event rows.

## Output
Every part's own lines (below), followed by a trailing `MALFORMED <n>` line reporting how many
`EVENTS` rows for **that part's invocation** were skipped as malformed (`n` may be `0`). Part 4
additionally appends a `DROPPED <n>` line (late-arrival drops, see below) directly before
`MALFORMED`. All numeric aggregate fields (`sum`, `avg`, `p50`, `p90`) are formatted with
Python's `f"{x:.2f}"` — always two decimal digits, and ties round the same way `.2f` rounds a
`float` (round-half-to-even on the underlying binary value) — do not implement your own decimal
rounding, match `.2f` exactly, since that is what the hidden tests were generated with.

## Rules

### Part 1 — parse and aggregate by (name, labels)
Group every well-formed event by `(metric_name, canonical_labels)`. For each group with at least
one event, compute `count` (int), `sum` and `avg` (float, `.2f`). Output one line per group,
**sorted by `metric_name` ascending, ties broken by `canonical_labels` ascending** (`S08`):
```
<metric_name>,<labels> count=<c> sum=<s> avg=<a>
```
`<labels>` is the canonical form (`-`, or sorted `key=value;...`).

### Part 2 — windowed buckets with count/avg/percentiles
For every `(metric_name, canonical_labels, window k)` combination that has at least one matching
event (`k*step <= timestamp < k*step + size`), compute `count`, `avg`, and two percentiles over
that window's matching `value`s using **nearest-rank**: sort the values ascending, then
`p<P> = values[ceil(P/100 * n) - 1]` (1-indexed rank clamped into `[1, n]`, i.e. `p50` of a
4-value window uses rank `ceil(0.5*4)=2` -> the 2nd-smallest value). Output one line per
combination, **sorted by `metric_name`, then `canonical_labels`, then `k`, all ascending**:
```
<metric_name>,<labels>,window=<k> count=<c> avg=<a> p50=<p50> p90=<p90>
```
A single-window-membership event under a sliding (`step < size`) configuration appears in
**every** window `k` whose range contains its timestamp — it is not an error or a duplicate, it
is the defined behavior of an overlapping window.

### Part 3 — alerting with trigger/clear hysteresis
For every window `k` from `0` to `max_k` (the largest window index touched by **any** well-formed
event in the whole stream — shared across every rule, so a rule's own metric can go silent for a
stretch and that silence is still walked as a sequence of empty, `0`-valued windows, not skipped),
evaluate every rule's `stat` against its `(metric_name, labels)`'s matching events in window `k`,
compare it to `threshold` via `op`, and run this state machine **per rule**, independently:

* Start in state `OK`, with `consecutive_true = 0` and `consecutive_false = 0`.
* At each window `k`, if the rule's condition is true: `consecutive_true += 1`,
  `consecutive_false = 0`; if false: `consecutive_false += 1`, `consecutive_true = 0`.
* In state `OK`: once `consecutive_true == trigger_n`, flip to `FIRING` and emit a transition
  line for window `k`; reset `consecutive_true = 0` (so a rule with `trigger_n = 1` re-fires
  immediately if it needs to — see Part 4's re-trigger edge case).
* In state `FIRING`: once `consecutive_false == clear_n`, flip back to `OK` and emit a
  transition line for window `k`; reset `consecutive_false = 0`.
* Nothing is emitted for a window that doesn't flip the state.

Output, **for every rule in the order it appears in the `RULES` section** (input order, not
sorted — a rule's own transitions are chronological by construction), one line per transition:
```
<metric_name>,<labels> ALERT_ON window=<k>
<metric_name>,<labels> ALERT_OFF window=<k>
```
A rule that never transitions prints nothing (not even a header line).

### Part 4 — out-of-order arrival and late-window drops
Same `WINDOW`/`RULES` semantics as Part 3, plus a streaming watermark over the `EVENTS` section
**processed in the given line order** (not re-sorted by timestamp — this is the out-of-order
arrival case): each event's **primary bucket** is `p = timestamp // step` (its native bucket by
`step`, independent of how many sliding windows it may also contribute to). Track
`max_primary_seen` (highest `p` seen among **incorporated** events so far, `-1` before the first
one). Before incorporating a new well-formed event with primary bucket `p`:
* if `p < max_primary_seen - L` (`L` from `LATENESS`), the event is **too late** — drop it
  (do not aggregate it into any window), and count it in the `DROPPED` tally;
* otherwise incorporate it normally (into every sliding window whose range contains its
  timestamp, exactly as Part 2/3 would), and update `max_primary_seen = max(max_primary_seen, p)`.

After all events are processed (with late ones excluded), run **exactly** Part 3's rule
evaluation over the final aggregated data and emit the same transition-line output, then
`DROPPED <n>`, then `MALFORMED <n>`.

## Worked examples
```
# Part 1
EVENTS
0,latency,region=us,120
5,latency,us=1;region=us,80
10,latency,region=eu,300
not,a,valid,row,extra
-->
latency,region=eu count=1 sum=300.00 avg=300.00
latency,region=us count=1 sum=120.00 avg=120.00
latency,region=us;us=1 count=1 sum=80.00 avg=80.00
MALFORMED 1
```
(the second `latency` row's labels are `us=1;region=us` -- canonical form sorts the pairs, giving
`region=us;us=1`, a **different** series from plain `region=us`, so it does NOT merge into the
first group even though `region=us` is a substring of both; sorted by `metric_name` then
`canonical_labels`, `region=eu` sorts before `region=us` before `region=us;us=1`.)

See `solution.py` and `test_q41.py` for the fully-worked Part 2/3/4 numbers (window bucketing,
percentile ranks, and the alert transition log) — they were produced by running the reference
solution on the exact input shown, not computed by hand, the same discipline `ps11`'s problem.md
asks you to hold worked examples to.

## Edge cases hidden tests are known to target
- Part 1: label pairs given in different orders across rows that must still merge into one
  series; the `-` no-labels sentinel; every one of the four malformed-row reasons (wrong field
  count, non-integer timestamp, non-float value, malformed labels string) tallied correctly.
- Part 2: a value exactly on a percentile rank boundary (`p50` of an even-length window); a
  sliding configuration where one event contributes to two or three overlapping windows; a
  tumbling configuration (`step == size`) producing no overlap at all.
- Part 3: `gt` vs `gte` and `lt` vs `lte` at the exact threshold value; `trigger_n = 1` (fires on
  the very first true window); a silent stretch (a rule's metric stops reporting entirely) still
  advancing `consecutive_false` because the shared `max_k` walk doesn't skip empty windows; a
  rule that fires, clears, and fires again (two separate `ALERT_ON` lines); `rate` with a window
  that has zero matching events (`0.0`, never a crash, and never true unless `op` accepts `0.0`).
- Part 4: an event that arrives late but still within `L` windows of tolerance (incorporated
  normally, no drop); an event beyond `L` (dropped, tallied, and provably absent from the alert
  evaluation — construct a case where including vs excluding it changes an `ALERT_ON` line);
  `L = 0` (any out-of-order arrival behind the current max primary bucket is dropped).
- Format: every aggregate number is exactly two decimals via `.2f` semantics; `MALFORMED`/
  `DROPPED` always present (even `0`); labels canonicalization never reorders across parts
  inconsistently.

## Variants seen in the wild
None known — this is a from-scratch reconstruction (see the confidence note above), not a
documented variant list from a real source.

## Sources
- `catalog/discovery/2026-09/C_batchA.md` `## C1 · Observability` (2026-09-03 discovery pass —
  the only evidence this problem is built from: a confirmed title, no body).
- https://www.interviewdb.io/question/stripe/observability (title confirmed via WebFetch; body
  is a client-rendered placeholder, "No questions are available yet").
- PracHub "Design a Count-Metrics Monitoring Platform" (onsite system-design question, cited in
  `C_batchA.md` as thematic corroboration only — not a source for any rule in this file).

## What this tests
skills: **S02** line-oriented parsing with an explicit malformed-row tally and label-string
canonicalization · **S12** time-bucket arithmetic (`timestamp // step`, half-open window ranges)
· **S05** threshold semantics (`gt`/`gte`/`lt`/`lte` strict vs non-strict; `count` vs `rate`
volume-vs-ratio) · **S10** an event-driven state machine with explicit transitions (`OK` <->
`FIRING`, only transitions are emitted) · **S16** sliding-window bucketing (`step < size`,
overlapping window membership) · **S08** deterministic multi-key sort (Part 1/2's grouping order)
and explicit input-order preservation where sorting would be wrong (Part 3/4's per-rule
transition order) · **S09** exact two-decimal formatting pinned to `.2f` semantics, always-present
trailer lines (`MALFORMED`/`DROPPED`) even at zero.
