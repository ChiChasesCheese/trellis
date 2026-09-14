---
id: reliability-latency-sli-form
node: reliability.slo
type: qa
---
## Q
Why do SRE teams define a latency SLI as "% of requests faster than 300ms" instead of "p99 < 300ms"?

## A
The threshold form turns latency into a **good-event / total-event ratio**, which:

- Plugs directly into **error-budget math** — each slow request spends budget, same as an error.
- **Aggregates cleanly** across shards, regions, and time windows (counts add; percentiles don't — [[reliability-percentile-aggregation]]).
- Reflects users: it counts *how many* requests were slow, while a p99 target says nothing about how bad the worst 1% was or how many users it hit.

Also specify **where** it's measured (load balancer vs client) — client-side includes network reality but adds noise you don't control.

## Q zh
为什么 SRE 团队将延迟 SLI 定义为"% 的请求快于 300ms"而不是"p99 < 300ms"？

## A zh
阈值形式将延迟变成**好事件 / 总事件比率**，这：

- 直接插入**error-budget 数学** ——每个慢请求花费预算，与错误相同。
- **干净聚合**跨分片、区域和时间窗口（计数相加；百分位不——[[reliability-percentile-aggregation]]）。
- 反映用户：它计数*多少个*请求很慢，而 p99 目标对最坏 1% 有多坏或它击中多少用户什么都不说。

也指定**哪里**被测量（负载均衡器 vs 客户端）——客户端包括网络现实但添加你不控制的噪音。
