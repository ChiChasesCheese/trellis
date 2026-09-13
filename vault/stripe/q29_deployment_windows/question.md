# q29 · Weekly Deployment Window Scheduler — first K valid UTC deployment windows

## Context
Stripe deploys its API to many regions. A deploy must never land while any region is inside its
local **business hours** (support load is highest, so deploys are frozen). Each region reports its
hours in *local* time with a fixed UTC offset (`+9`, `-8`, `+5.5` — no DST, no `zoneinfo`).
The release tooling needs the UTC intervals of a day during which **no** region is in business
hours, then the first K such windows of at least L minutes starting from "now", skipping
company-wide blackout dates, and finally a weekly view where each region has weekday-specific hours.
Minute granularity everywhere.

## Input (stdin)
First line `PART n` (1–4). Then a header line whose shape depends on the part, followed by
region rules, one per line. Blank lines are ignored; spaces around commas are tolerated.

Region rule (Parts 1–3): `name,utc_offset_hours,local_start,local_end`
Region rule (Part 4):    `name,utc_offset_hours,days,local_start,local_end`
Blackout (Parts 3–4):    `blackout,YYYY-MM-DD` (a whole UTC day, may appear anywhere after the header)

- `utc_offset_hours`: decimal hours with optional sign, e.g. `+9`, `-8`, `5.5`, `-3.5`, `+5.75`.
  Local time = UTC + offset, so **UTC = local − offset**.
- `local_start`, `local_end`: `HH:MM`, business hours are the half-open interval `[start, end)`.
  If `end < start` the window wraps past local midnight (`22:00,06:00` = 22:00 → 06:00 next day).
  If `end == start` the region is busy the whole day (24 h). (reconstructed)
- `days` (Part 4 only): weekday names `Mon Tue Wed Thu Fri Sat Sun`, joined by `/`, with `-`
  ranges: `Mon-Fri`, `Sat/Sun`, `Mon-Wed/Fri`. The weekday is that of the region's **local** date.
  A region may appear on several lines (different hours on different days).
- The same 4-field rule in Part 4 (no `days`) means every day.

Header per part:
| Part | header | meaning |
|---|---|---|
| 1 | `YYYY-MM-DD` | the *local* business date to convert |
| 2 | `YYYY-MM-DD` | the *UTC* day to analyse |
| 3 | `YYYY-MM-DDTHH:MM,L,K` | UTC "now", minimum window length in minutes, number of windows wanted |
| 4 | `YYYY-MM-DD,L` | first UTC day of the 7-day week to list, minimum window length |

## Output
One line per result. A window is printed as `YYYY-MM-DDTHH:MM..HH:MM` — the UTC start
datetime, then the end *time* on the same UTC day; a window reaching midnight ends with `24:00`.
Windows **never cross a UTC midnight** — a free stretch that spans midnight is split into two
windows, each judged against L on its own. (reconstructed; consistent with per-day blackouts)

## Rules
### Part 1 — local business hours → UTC (reconstructed from "UTC Timezone Mapping")
For each rule, in input order, print `name START..END` where START/END are the UTC datetimes
(`YYYY-MM-DDTHH:MM`) of that region's business hours on the given local date. Handle fractional
offsets (`+5.5` → 330 min) and day wrap (a `+11` region's 09:00 is 22:00 UTC the previous day).

### Part 2 — free UTC intervals of one UTC day (reconstructed)
For the given UTC day `[00:00, 24:00)`, compute every region's business-hour intervals that touch
the day (a region's local dates D−1, D, D+1 can all spill into UTC day D), clip them to the day,
take the union, and print the **complement** as maximal windows, ascending. Adjacent/overlapping
busy intervals merge; a fully free day prints `YYYY-MM-DDT00:00..24:00`; a fully busy day prints
nothing.

### Part 3 — first K windows of length ≥ L from "now", skipping blackout dates
Scan UTC days forward from the header datetime. Blackout days are skipped entirely. On the first
day, windows are clipped to start no earlier than "now" (`08:30` inside a free `08:00..09:00`
gives `08:30..09:00`). Keep windows whose length is **≥ L** (`>=`, a 30-minute window qualifies
for L=30). Stop after K windows. Scanning stops after 366 days; if fewer than K windows exist by
then, print the ones found (possibly nothing). `K = 0` prints nothing.

### Part 4 — weekly recurrence (weekday-specific hours) (reconstructed)
Rules now carry `days`. A rule contributes business hours only on local dates whose weekday is in
`days`. List **every** window of length ≥ L for the 7 UTC days starting at the header date (no K
cap, no "now" clipping), still skipping blackout dates.

## Worked examples
**Part 1** — local date 2026-03-02
```
PART 1
2026-03-02
tokyo,+9,09:00,17:00
india,+5.5,09:00,17:00
london,0,09:00,17:00
us-west,-8,09:00,17:00
sydney,+11,09:00,17:00
```
```
tokyo 2026-03-02T00:00..2026-03-02T08:00
india 2026-03-02T03:30..2026-03-02T11:30
london 2026-03-02T09:00..2026-03-02T17:00
us-west 2026-03-02T17:00..2026-03-03T01:00
sydney 2026-03-01T22:00..2026-03-02T06:00
```

**Part 2** — UTC day 2026-03-02 with tokyo(+9), london(0), us-west(−8), all 09:00–17:00
busy: tokyo 00:00–08:00 · london 09:00–17:00 · us-west 17:00–24:00 (Mon) and 00:00–01:00 (Sunday's
shift spilling over) → union `[00:00,08:00] ∪ [09:00,24:00]` → one free hour:
```
2026-03-02T08:00..09:00
```

**Part 3** — same three regions, now = 2026-03-02T08:30, L=30, K=3, blackout 2026-03-03
```
PART 3
2026-03-02T08:30,30,3
blackout,2026-03-03
tokyo,+9,09:00,17:00
london,0,09:00,17:00
us-west,-8,09:00,17:00
```
```
2026-03-02T08:30..09:00
2026-03-04T08:00..09:00
2026-03-05T08:00..09:00
```
(with L=45 the clipped first-day window is only 30 min, so the answer is 03-04, 03-05, 03-06.)

**Part 4** — week starting Monday 2026-03-02, L=60, the same regions but Mon–Fri only
```
PART 4
2026-03-02,60
tokyo,+9,Mon-Fri,09:00,17:00
london,0,Mon-Fri,09:00,17:00
us-west,-8,Mon-Fri,09:00,17:00
```
```
2026-03-02T08:00..09:00
2026-03-03T08:00..09:00
2026-03-04T08:00..09:00
2026-03-05T08:00..09:00
2026-03-06T08:00..09:00
2026-03-07T01:00..24:00
2026-03-08T00:00..24:00
```
Saturday 03-07 UTC still carries us-west's Friday shift until 01:00 UTC; Sunday is fully free
(tokyo's Monday starts at 2026-03-09T00:00 UTC, outside the week).

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s12-time-and-dates|S12 时间与日期]]
- [[s13-closed-intervals-offbyone|S13 闭区间、补齐空隙、off-by-one 纪律]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
