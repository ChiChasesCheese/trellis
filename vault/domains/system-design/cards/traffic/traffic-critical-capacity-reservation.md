---
id: traffic-critical-capacity-reservation
node: traffic.rate-limiting
type: qa
---
## Q
When an API fleet saturates, dropping low-priority traffic first is the obvious move. How does *reserving capacity* for critical requests (Stripe-style fleet-usage shedding) differ from reactive priority shedding, and why keep the reservation even when the fleet is healthy?

## A
- **Reactive priority shedding** waits for distress signals (queue depth, latency, CPU) and then drops the least important traffic first. It works, but it engages only after the system is already hurting.
- **Capacity reservation** classifies methods up front — core operations that move money (e.g. charge creation) vs everything else (listing, analytics, dashboards) — and **reserves a fixed fraction of fleet workers that only critical traffic may occupy**. Non-critical requests start getting rejected as soon as total usage crosses the *unreserved* share, before saturation.
- Keeping the reservation always-on is the point: it is a **static guarantee**, not a reaction — a sudden non-critical flood (a merchant's batch job, a scraper) physically cannot occupy the last workers, so the API's core stays alive even when overload arrives faster than any health signal can trip.

## Q zh
API 集群饱和时，先丢低优先级流量是显而易见的一招。为关键请求*预留容量*（Stripe 风格的 fleet-usage shedding）与被动的按优先级丢弃有何不同？为什么集群健康时也要保持这份预留？

## A zh
- **被动的优先级丢弃**等待压力信号（队列深度、延迟、CPU）出现，然后先丢最不重要的流量。它有效，但只在系统已经受伤之后才介入。
- **容量预留**预先给方法分类 — 移动资金的核心操作（如创建 charge）vs 其余一切（列表、分析、仪表盘）— 并**预留固定比例的集群 worker，只允许关键流量占用**。一旦总用量越过*非预留*份额，非关键请求就开始被拒绝，早于饱和点。
- 预留常开正是关键：它是**静态保证**，不是反应 — 突发的非关键洪峰（某商户的批处理任务、一个爬虫）物理上无法占据最后那部分 worker，所以即使过载来得比任何健康信号跳闸都快，API 的核心也活着。
