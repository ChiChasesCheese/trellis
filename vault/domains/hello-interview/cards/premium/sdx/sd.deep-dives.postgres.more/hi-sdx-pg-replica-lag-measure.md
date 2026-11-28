---
id: hi-sdx-pg-replica-lag-measure
node: sd.deep-dives.postgres.more
type: qa
step: 1
---
## Q
**Postgres 副本延迟：怎么量，为什么会突然飙**｜补充 · PostgreSQL · 追问

面试官：「你跑了 Postgres 只读副本。复制延迟具体怎么量，有哪两个单位？网络没问题时，什么负载会让它突然变大？」

## A
**结论。** 两个单位都要量：字节（落后多少 WAL）和秒（最后一条回放的记录有多旧）。突发写入和副本上的长查询是常见原因，两者要配对告警。

**要点。**
- **字节：** 副本已应用的 WAL 位置（LSN）比主库落后多少，是真实积压量，写入忽快忽慢时更可靠。
- **秒：** 最后回放的记录有多旧，是用户感受到的陈旧程度。主库空闲时「秒」可能很大而没有任何积压，所以两个一起告警。
- **写入突发：** 批量导入、大迁移、大批删除产生 WAL 的速度，超过副本单个回放进程能应用的速度。
- **回放和查询冲突：** 回放清理操作会让副本上长查询还要读的旧行失效，副本要么暂停回放（延迟增长，等待上限由 `max_standby_streaming_delay` 控制，默认 30 秒），要么取消查询。
- **副本反馈：** `hot_standby_feedback`，副本告诉主库自己还需要哪些旧版本，避免取消查询，代价是主库清理被拖住、表膨胀。默认关闭。
- **为什么要告警：** 延迟既是读到陈旧数据的窗口，主库挂了时也是故障转移的丢数据窗口。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 330">
<rect x="10" y="8" width="150" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库</text>
<text x="85.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">WAL 位置 LSN 1000</text>
<rect x="180" y="8" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本</text>
<text x="255.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已回放 LSN 940</text>
<polyline points="160,28 173.0,28.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,28 173.0,31.2 173.0,24.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">字节落后 = 主库 LSN − 回放 LSN</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">秒落后 = 现在 − 最后回放记录的时间</text>
<rect x="10" y="116" width="320" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="132.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回放清理记录，会让副本长查询</text>
<text x="170.0" y="147.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还要读的旧行失效：冲突</text>
<polyline points="85,156 85.0,189.0" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="85,196 81.8,189.0 88.2,189.0" fill="currentColor"/>
<polyline points="255,156 255.0,189.0" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="255,196 251.8,189.0 258.2,189.0" fill="currentColor"/>
<rect x="10" y="196" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="212.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">暂停回放</text>
<text x="85.0" y="227.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">延迟增长</text>
<rect x="180" y="196" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="212.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或取消查询</text>
<text x="255.0" y="227.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">报冲突错误</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">hot_standby_feedback：保住查询，</text>
<text x="8" y="280" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">但主库清理被拖住、表膨胀</text>
<text x="8" y="306" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空闲主库上「秒」会虚高，</text>
<text x="8" y="324" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以字节和秒一起告警</text>
</svg>

**面试里这样说。** 「我同时监控字节和秒两个延迟。突发写入和副本长查询是常见原因：长查询和回放冲突要么拖慢回放，要么被取消；开 `hot_standby_feedback` 会保住查询，但主库清理会被拖住。分析型长查询我不放在要求低延迟的副本上。」

**易错。**
- **只看秒：** 空闲主库上秒数看起来很大，却没有真实积压，容易误报。
- **随手开 `hot_standby_feedback`：** 副本上的一个长查询会让主库无法清理死元组，主库表膨胀。
