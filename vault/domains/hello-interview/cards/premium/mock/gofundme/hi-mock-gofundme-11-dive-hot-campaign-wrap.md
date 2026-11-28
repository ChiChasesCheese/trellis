---
id: hi-mock-gofundme-11-dive-hot-campaign-wrap
node: fix.gofundme-mock
type: qa
step: 11
---
## Q
**GoFundMe · 第 11 步 · 深入四：热点总额，以及收尾**｜模拟面试

面试官：「如果一个活动一秒钟来 5,000 笔捐款，同一行 campaign_totals 被抢着更新，你怎么办？最后请你用一分钟把整个设计过一遍。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先量：** 现在 100 笔/秒、每笔一个短事务，一行排队够，不改；极端 5,000 笔/秒时一行每秒只能串行几百次，会排队、超时、总额落后。
- **不变前提：** 不管怎么改，worker 先 INSERT applied(donation_id)，只对真正插入的行加总。
- **方案一，批量：** worker 一次取最多 200 条事件，`INSERT applied … ON CONFLICT DO NOTHING RETURNING 金额`，把返回的新插入金额求和，一次 UPDATE：5,000 ÷ 200 = 25 次/秒更新这一行；展示晚几十毫秒，活动页本有 5 秒缓存，可接受。
- **方案二，分片：** campaign_totals 变成每活动 16 行，shard = hash(donation_id) % 16，5,000 ÷ 16 ≈ 312 次/秒一行；读时要 SUM 16 行，只在 worker 里算再 SET 到 Redis。
- **选批量：** 只改 worker，读路径不变；不够或要多个 worker 并行时再加分片。两种都经过已应用表，重放不会多算。
- **捐款路径：** 每笔是自己的一行，没有共享行；共享的是 PSP 额度：5,000 × 0.5 秒 = 2,500 个并发调用，要提前约额度，超出先返回 Pending。
- **一分钟收尾：** 客户端先生成 K，服务端先提交 Pending 再带 D1 调 PSP；只有 Success 发事件，worker 用已应用表只加一次，Redis 只是副本；活动页读两个有界 sorted set，前面是 CDN；对账按 D1 查 PSP 收掉 Pending。
- **只剩 45 分钟：** 深入三和四各压到 3 分钟，深入一和二不能删。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 342">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">热门活动：同一行被抢着加</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">现在：100 笔/秒 → 一行</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每笔一个短事务，行锁排队也还够</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 不动；先量，再改</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">极端：5,000 笔/秒 → 一行</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一行每秒只能串行几百次</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 排队、超时、总额落后</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">方案一：批量 200 条一个事务</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5,000 ÷ 200 = 25 次/秒更新这一行</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 展示晚几十毫秒</text>
<rect x="8" y="236" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="256" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">方案二：分 16 行（按 id 哈希）</text>
<text x="18" y="271" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5,000 ÷ 16 ≈ 312 次/秒/行；读时求和</text>
<text x="18" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 读多一步 SUM，多个 worker 并行</text>
<text x="8" y="314" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两种都先 INSERT applied(donation_id)，</text>
<text x="8" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只对新插入的行求和、加总</text>
</svg>
白板上新增：worker 改成批量；这一张就是最后的完整白板。

**常见失分。**
- **一听热点就分片：** 100 笔/秒分片是过早优化，先量再改。
- **改动绕过已应用表：** 批量或分片后重放仍会多算。
- **收尾没有主线：** 只列组件，说不清键、先写后调、只加一次、有界读、对账这条线。

**面试官可能接着问。**
- 总额以后怎么对账？ → 每天用 donations 的 Success 求和对比 campaign_totals，偏差大就告警重算，不在热路径。
- 批量里一条重放消息？ → 在 applied 里冲突，RETURNING 不返回它，不进求和，其他条目照常。
- 为什么不直接分片？ → 分片让读多一步求和、热点变多行；批量只改 worker，先改动小的，数字证明不够再加。
