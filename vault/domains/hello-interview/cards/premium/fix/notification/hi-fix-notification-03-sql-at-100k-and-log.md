---
id: hi-fix-notification-03-sql-at-100k-and-log
node: fix.notification
type: qa
step: 3
---
## Q
**通知系统 · 单库扛不住 10 万写/秒，前面放什么**｜复盘

面试官：「你说一个 SQL 数据库存所有请求。尖峰 10 万写每秒，一个 SQL 库能扛住吗？你会在它前面放什么？」

你会怎么回答？

## A
**当时的回答。** 11:28 先说「需要一个库存请求」，本能对；面试官 11:30 问库能不能扛 10 万写，你 12:23 才说放进 Kafka，晚了约 6 分钟；只说「hard for normal SQL databases」，没有一个数对比 100K，也没说日志带来什么新问题。

**应该这样说。**
- **先说决定：** 尖峰 83,000 写/秒，单库舒适区约 20,000（调优良好的 Postgres 简单写），所以请求先写进日志，worker 按库的速度写。没有数字的「扛不住」不可信。
- **数字撑它：** 平均 5,800 写/秒单库够，只有尖峰需要日志；尖峰 120 秒积压 (83,000 − 20,000) × 120 ≈ 7,600,000 条，库净排空速度 14,200 条/秒，约 9 分钟排空。
- **职责：** 日志吸收尖峰；崩溃后消息还在，worker 从 offset 继续。
- **新问题：** 会重复投递，库里用唯一键吸收；会积压，监控 lag 和最老消息的年龄。
- **成本：** 7 天保留 5,800 条/秒 × 1 KB × 86,400 × 7 ≈ 3.5 TB，三副本约 10 TB。
- **触发：** 稳态就超过库上限时，日志只是把过载推后，要先分片；尖峰只有 5,000 写/秒就不加日志。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">加日志：职责、代价、触发，各一句</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">职责</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">吸收 83,000/秒 的尖峰，库按 20,000/秒 写</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">崩溃后消息还在，worker 从偏移量继续</text>
<rect x="8" y="93" width="324" height="74" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">新问题和处理</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重复投递 → 唯一键吸收</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">积压 → 监控 lag 和最老消息年龄</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">成本：7 天 × 500 GB/天 ≈ 3.5 TB</text>
<rect x="8" y="175" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">触发</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">尖峰 &gt; 单库写上限：才加</text>
<text x="18" y="223.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">稳态 &gt; 库上限：日志只掩盖过载</text>
</svg>
白板上：上面是没有日志时的两个速率，下面是有日志时的积压；右边三格是职责、新问题、触发。

**常见失分。**
- **只说「SQL 扛不住」：** 没有 20,000 这个对比数。
- **把日志当永远的答案：** 稳态超过库就不是日志能解决的。
- **加了日志不说重复和积压：** 等于没说新问题。

**面试官可能接着问。**
- 日志挂了？ → 拿不到持久化就不能返回 202，返回 503 让调用方重试；日志三副本，挂一台不影响。
- 回执会排在营销后面吗？ → 同一个 topic 会；按优先级拆成两个 topic、两组 worker，是下一个深入点。
- 为什么不用 Redis 队列？ → 主从切换会丢最近的写，回执不能丢；日志要 acks=all。
