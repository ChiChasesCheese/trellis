---
id: distributed-monotonic-vs-wallclock
node: distributed.time.clocks
type: qa
---
## Q
Time-of-day clock vs monotonic clock — which do you use for timeouts and elapsed-time measurement, and what goes wrong if you pick the other?

## A
**Monotonic** for all durations (timeouts, latency measurement, rate limiting): it only moves forward, at a steady rate. Its absolute value is meaningless and **not comparable across machines** — it's typically time since boot.

**Time-of-day** clocks are NTP-disciplined: they get **slewed** (rate-adjusted) for small errors but **stepped** — jumped, possibly *backwards* — for large ones, and they pause weirdly across VM migrations and leap-second smearing. Measuring an interval with wall-clock time can therefore yield negative or wildly wrong durations; classic bugs: request "timeouts" firing instantly after an NTP step, or negative latency metrics.

Rule: wall clock only for timestamps humans or other systems interpret as calendar time — and never for ordering writes ([[distributed-lww-danger]]).

## Q zh
日期-时间时钟 vs 单调时钟 — 用于超时和耗时测量时选哪个？选另一个会发生什么？

## A zh
**单调时钟**用于所有时间段（超时、延迟测量、速率限制）：它只向前移动，速率稳定。其绝对值无意义且**不能跨机器比较** — 通常是自启动以来的时间。

**日期-时间时钟**受 NTP 管理：对小错误**调整速率**（slew），但对大错误**跳跃** — 可能*向后退* — 并在虚拟机迁移和闰秒处理中表现异常。用 wall-clock 时间测量间隔可能导致负时间或极度错误的值；常见 bug：NTP 跳跃后请求超时立即触发，或负延迟指标。

规则：wall-clock 只用于人类或其他系统解释为日历时间的时间戳 — 永远不要用于排序写入（[[distributed-lww-danger]]）。
