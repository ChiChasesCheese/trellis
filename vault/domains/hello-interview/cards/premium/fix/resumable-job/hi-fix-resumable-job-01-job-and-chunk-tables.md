---
id: hi-fix-resumable-job-01-job-and-chunk-tables
node: fix.resumable-job
type: qa
step: 1
---
## Q
**通知系统 · 活动扇出的进度存在哪**｜补强

面试官：「一个营销活动要发给 1,000 万用户。扇出任务跑到 400 万的时候进程挂了。重启之后，是什么状态告诉它前 400 万已经处理过？这个状态存在哪里？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **存在数据库，两张表：** 任务表 `campaign_job` 一行，块表 `campaign_chunk` 一千行；不放进程内存，也不靠供应商 webhook。
- **先冻结受众：** 发起时把 1,000 万个 user_id 写进快照表 `campaign_audience`，seq 从 1 连续编号；否则重启后重新查询，人群变了，「前 400 万」就没有意义。
- **切块：** 1,000 万 ÷ 10,000 = 1,000 块，块 k 管 seq 区间 [(k−1)×10,000+1, k×10,000]；块表每块一行：pending / claimed / done，另有 claimed_by、lease_until。
- **关键事务：** 处理一块 = 一个事务：INSERT 这块 10,000 行消息（`campaign_message`，同时是发件箱，`(campaign_id, user_id)` 唯一，ON CONFLICT DO NOTHING）加 UPDATE 本块为 done。状态先提交，崩了这块标 done 却没消息，10,000 人永远收不到；消息先提交，崩了这块被重做，靠唯一键兜底；同事务两种都不会出现。
- **块大小：** 消息行约 100 字节，10,000 行 = 1 MB 的事务，崩溃最多重做 0.1%。
- **节奏：** 活动配额假设 20,000 条/秒（回执另有预留）= 2 块/秒，1,000 块约 500 秒 ≈ 8.3 分钟，在分片库的写入舒适区内。
- **单 worker：** 顺序跑，任务行放一个 cursor（已完成的最大 seq）和消息同事务更新就够；并行才需要块表。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1,000 块的状态条（崩溃的那一刻）</text>
<rect x="8" y="28" width="129.6" height="26" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="72.8" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">done × 400</text>
<rect x="137.6" y="28" width="4.0" height="26" stroke-width="1.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="141.6" y="28" width="194.1" height="26" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="238.638" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">pending × 599</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">400 块 done = 400 × 10,000 = 4,000,000 人</text>
<text x="8" y="93" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 401 块在跑：事务没提交，回滚，仍是 claimed</text>
<text x="8" y="110" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重启：第一个不是 done 的块 = 401</text>
</svg>
白板上：四张表的字段，一个事务框（消息行 + 块变 done），底下一条 1,000 块的状态条。

**常见失分。**
- **答成 webhook 和限流：** 被问两遍「什么状态记录进度」，答的是分批、限流器，不是进度。
- **进度放进程内存：** 一挂就没了，正是被问的失败。
- **块状态和消息分开提交：** 状态先提交永久丢人；消息先提交块被重做。
- **没有冻结受众：** 重启后「前 400 万」已是另一批人。
- **一个大事务装 1,000 万行：** 约 1 GB，崩溃全部重来，锁和日志都撑不住。

**面试官可能接着问。**
- 消息直接发日志，不写发件箱？ → 日志和库之间没有事务：先发布、等 `acks=all`，再标 done；崩溃最多半块重发，由唯一键或下游去重吸收；反过来先标 done，崩溃会丢整块。
- 为什么不只放游标？ → 一个 worker 够；10 个并行就要每块一个状态，否则重叠或漏块，游标是块表的特例。
- 块多大？ → 100 行一块有 100,000 块；1,000,000 行一块是 100 MB 事务、重做 10%；10,000 行折中。
- 谁来发行？ → sender 用 `FOR UPDATE SKIP LOCKED` 取 pending 行，过限流器，成功标 sent；也可由中继追加到日志分区。
- 为什么这里不要日志挡前面？ → 活动是我们自己发起、自己定节奏，20,000 行/秒是自选上限，库扛得住；回执速率不归我们定。
- 快照后退订？ → 调供应商前再查一次，已退订的标 skipped；快照只决定谁在名单上。
