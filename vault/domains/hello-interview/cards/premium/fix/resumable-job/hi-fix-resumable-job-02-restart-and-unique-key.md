---
id: hi-fix-resumable-job-02-restart-and-unique-key
node: fix.resumable-job
type: qa
step: 2
---
## Q
**通知系统 · 重启后从哪一块继续**｜补强

面试官：「进程重启了。它怎么知道从哪里继续、不把前 400 万再发一遍？它崩溃的时候正好在写一块，会不会有人收到两条？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **从哪里继续：** 读块表，第一个不是 done 的块就是游标；400 块 done = 4,000,000 人已处理，前 400 块一行都不再碰。可信是因为 done 和这块的消息行同一个事务：标了 done 一定有消息，没标 done 的块一行消息都没有。
- **崩在块 401 里：** 事务没提交、整块回滚，块仍是 claimed；租约 2 分钟（一块正常不到 1 秒）到期后另一个 worker 重新认领。
- **重叠仍会出现：** 一，被判死的 worker 只是慢，两个都跑了块 401；二，扇出若不先落库而是直接追加到日志，事务管不到日志，崩在发出 4,000 条后重跑会把这块 10,000 条再发一遍。
- **唯一键吸收：** 消息行 `UNIQUE (campaign_id, user_id)` + `ON CONFLICT DO NOTHING`，4,000 个冲突被跳过，只新增 6,000 行；受影响 1 行才发，0 行跳过。重叠上限每个 worker 一块：10 × 10,000 = 100,000，占 1%，全被吸收。
- **为什么不用锁、不先查：** 先查是每块 10,000 次 SELECT，两个 worker 同时查都看到「没有」；唯一键一条语句由数据库原子裁决。
- **坏块：** 块表加 attempts，同一块失败 3 次标 failed 并告警，其余块继续跑。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 218">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重跑块 401：唯一键吸收重叠</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">重跑块 401</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">尝试 INSERT 10,000 行</text>
<rect x="8" y="80" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">上次已写入 4,000 行</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNIQUE (campaign_id, user_id) 冲突</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ON CONFLICT DO NOTHING：跳过</text>
<rect x="8" y="149" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">新增 6,000 行</text>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4,000 + 6,000 = 10,000：每人一行</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每人只发一条</text>
</svg>
白板上：状态条上画出重启读到的位置 401；再画重跑块 401 时 4,000 个冲突、6,000 个新行。

**常见失分。**
- **只说「从上次的位置继续」：** 不说位置存在哪里。
- **位置只存在内存或日志偏移里：** 偏移只说明消费到哪，不说明扇出做到哪。
- **重启后整个活动重发：** 前 400 万人收到两条。
- **把唯一键当唯一防线：** 它只吸收重叠；不重做已完成的块靠块状态，两层各管一件事。

**面试官可能接着问。**
- 租约多长？ → 要比一块正常耗时长得多，否则误判慢 worker 为死；2 分钟的代价是真死了最多多等 2 分钟，对 8 分钟的活动可接受。
- 暂停或取消？ → 任务行 status 改 paused，worker 每次认领前先读，已认领的做完就停；恢复从第一个非 done 块继续。
- 写进库还没发出的行？ → 是 pending，sender 重启后照取；发供应商带 notification_id 做幂等键，供应商不支持时崩在「调用」和「标 sent」之间最多多发一批（至少一次的残余）。
- Kafka 事务能避免这个吗？ → 只在 Kafka 内部成立；库加消息只能用同事务的 outbox。
