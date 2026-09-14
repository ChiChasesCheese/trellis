---
id: cc-chrono-intervals-endpoints
node: chrono.intervals
type: cloze
---
With **inclusive** endpoints the gap between `[10, 20]` and `[25, 30]` is {{c1::`[21, 24]`}} — a filler ends at `next.start − 1`, never at `next.start` — and two intervals that merely touch, `end + 1 == next.start`, are {{c2::not a gap and produce no filler}}. With **half-open** `[a, b)` the same gap is {{c3::`[20, 25)`}} and touching means `end == next.start`. Choose one convention for the whole program and {{c4::write it in a comment above the state}}.

## zh
在**闭区间**约定下，`[10, 20]` 与 `[25, 30]` 之间的空隙是 {{c1::`[21, 24]`}} —— 填补区间结束在 `next.start − 1`，绝不在 `next.start` —— 而仅仅相接的两段（`end + 1 == next.start`）{{c2::不是空隙，不产生任何填补}}。在**半开区间** `[a, b)` 下，同样的空隙是 {{c3::`[20, 25)`}}，相接的判据是 `end == next.start`。整个程序只选一种约定，并 {{c4::在状态定义上方用注释写明}}。
