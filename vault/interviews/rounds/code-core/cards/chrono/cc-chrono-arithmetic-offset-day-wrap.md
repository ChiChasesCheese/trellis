---
id: cc-chrono-arithmetic-offset-day-wrap
node: chrono.arithmetic
type: qa
---
## Q
Regions report business hours in local time with a fixed UTC offset. You need every busy interval touching UTC day D. Why is converting only day D's local hours wrong?

## A
**`UTC = local − offset`, so one local day spills into the neighbouring UTC days.** A `+11` region's 09:00 local is 22:00 UTC on the *previous* day; a `−8` region's 17:00 local is 01:00 UTC on the *next* one.

- Build candidates from local dates **D−1, D and D+1**, convert each to UTC, then clip to `[D 00:00, D+1 00:00)`.
- A local window that wraps past midnight (`22:00 → 06:00`) is one interval crossing local midnight — handle it in the converter, not at every call site.
- `end == start` conventionally means the whole 24 hours, not an empty window; that reading has to be chosen explicitly.
- Do the whole thing in integer minutes since an epoch, so clipping is just `max`/`min` ([[cc-chrono-parsing-hhmm-minutes]]).

## Q zh
各区域用本地时间加固定 UTC offset 上报营业时间。你需要所有与 UTC 第 D 天相交的忙碌区间。为什么只转换第 D 天的本地时间是错的？

## A zh
**`UTC = 本地 − offset`，所以一个本地日会溢出到相邻的 UTC 日。** `+11` 区域的本地 09:00 是*前一天*的 22:00 UTC；`−8` 区域的本地 17:00 是*后一天*的 01:00 UTC。

- 候选集要取本地日期 **D−1、D、D+1**，各自转成 UTC，再裁剪到 `[D 00:00, D+1 00:00)`。
- 跨过午夜的本地窗口（`22:00 → 06:00`）是一个跨本地午夜的区间 —— 在转换器里处理，而不是在每个调用点。
- `end == start` 按惯例表示整整 24 小时而非空窗口；这个读法必须显式选定。
- 整个过程都用自某个 epoch 起的整数分钟，裁剪就只是 `max`/`min`（[[cc-chrono-parsing-hhmm-minutes]]）。
