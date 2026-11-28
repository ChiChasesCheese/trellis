---
id: hi-fix-bounded-read-02-gofundme
node: fix.bounded-read
type: qa
step: 2
---
## Q
**GoFundMe 活动页 · 有界读**｜补强

面试官：「活动页要显示最近的 100 笔捐款和最大的 10 笔，而且不能每次都读主数据库。你怎么做？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **页面读三样，都是固定大小的 Redis 结构，不碰捐款表：** 总额、最近 100 笔、最大 10 笔。
- **最近 100 笔：** `campaign:{id}:recent` 有序集合，成员 donation_id，分数是成功时间毫秒；成功时 `ZADD` 再 `ZREMRANGEBYRANK … 0 -101`，读 `ZRANGE … 0 99 REV`。
- **最大 10 笔：** `campaign:{id}:largest`，分数是金额（分）；`ZADD` 后 `ZREMRANGEBYRANK … 0 -11`，读 `ZRANGE … 0 9 REV WITHSCORES`。
- **何时更新：** 只在转到 SUCCESS 且已应用表确认是第一次处理时；PENDING、失败和重放都不动它们。
- **为什么不用列表：** `LPUSH` + `LTRIM` 遇到事件重放，同一个 id 出现两次，旧捐款还被推到最前；`ZADD` 同成员同分数是幂等的。
- **摘要：** 集合里只放 id；成功时写只读摘要 `donation:{id}`（展示名、金额、时间），页面一次 `MGET` 取最多 110 条，缺的回源按主键查一次。
- **读的代价：** 总额 `GET`、两次范围读、一次 `MGET`，4 条命令 2 次往返（`MGET` 要等 id），与捐款总数无关；一亿次浏览压在 20,000 秒是 5,000 页/秒，约 2 万条 Redis 命令/秒，单个 Redis 扛得住。
- **Redis 冷了重建：** 两条带索引的查询，`(campaign_id, created_at DESC)` 取 100 条、`(campaign_id, amount_cents DESC)` 取 10 条，都 `WHERE status = 'SUCCESS'`，每个活动重建一次。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个事件重放时</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">列表 LPUSH + LTRIM</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再推一次：同一个 id 在榜里出现两次</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">列表，旧捐款重放</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧 id 被推到最前面，被裁掉的又回来</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">有序集合 ZADD</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同成员同分数：什么也没变</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">有序集合，旧捐款重放</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分数最小，立刻又被裁掉</text>
</svg>
白板上：列表在重放时出错，有序集合不怕重放。

**常见失分。**
- **去讲分片和连接池：** 它们缓解写入和连接压力，没有回答页面读什么。
- **用列表接重放的事件：** 同一个 id 出现两次，旧的被推到最前面。
- **创建时就更新：** 没付成功的捐款出现在最近列表里。
- **不说重建：** Redis 一冷，页面读空或打回主库。

**面试官可能接着问。**
- 退款或删除的捐款？ → 从两个集合 `ZREM`；最大 10 笔少一条就用索引查询补回，退款少，重建频率低。
- 最大的为什么只留 10 条？ → 页面只显示 10 条；多留 50 条可免于退款后立刻重建，是拿内存换复杂度，先问产品。
- 页面还能再缓存吗？ → 能，API 实例把整页本地缓存 1 到 2 秒，同一活动的读者共用一份。
