---
id: correctness-outbox-relay-lag
node: correctness.outbox
type: qa
---
## Q
The outbox relay dies for 2 hours. What is the failure mode for the system, and what do you monitor to catch it?

## A
Writes keep succeeding — the outbox insert is in the local transaction — so the system stays **available**; events are delayed, not lost, and downstream views go **stale** silently. That's the pattern's point (broker/relay outage decoupled from the write path) and its trap: nothing user-facing errors.

Monitor:
- **Oldest-unpublished-row age** (SELECT min(created_at) WHERE unsent) — the true staleness signal; alert on seconds/minutes per your freshness SLO.
- Unsent **row count** growth rate, and relay publish error rate.

On recovery the relay drains the backlog in order — expect a duplicate/late-event burst downstream, which consumer dedup ([[correctness-outbox-mechanism]]) must absorb.

## Q zh
outbox relay 宕机 2 小时。系统的故障模式是什么，监控什么来抓住？

## A zh
写继续成功 — outbox 插入在本地事务中 — 所以系统保持**可用**；事件延迟不丢失，下游视图**陈旧**无声。这是模式的要点（broker/relay 故障与写路径解耦）和陷阱：无用户面错误。

监控：
- **最老未发布行年龄**（SELECT min(created_at) WHERE unsent）— 真正的陈旧信号；按你的新鲜度 SLO 在秒/分钟级告警。
- 未发送**行数**增长率，和 relay 发布错误率。

恢复时 relay 按顺序消干积压 — 预期下游重复/晚事件爆发，消费者去重（[[correctness-outbox-mechanism]]）必须吸收。
