---
id: hi-mock-gofundme-03-nonfunctional
node: fix.gofundme-mock
type: qa
step: 3
---
## Q
**GoFundMe · 第 3 步 · 非功能需求与估算**｜模拟面试

面试官：「再说说非功能需求。有没有什么数字想先算一下？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **正确性第一：** 「一次点击最多扣一次钱；绝不出现『扣了款但我们没记录』；已募金额只算成功的捐款，每笔只算一次。」
- **先定时间窗：** 「一天有 86,400 秒，但流量集中在白天。我取 20,000 秒（约 5.5 小时）作为忙时窗口。如果摊在全天只有 1 亿 ÷ 86,400 ≈ 1,157 次/秒，我按忙时算更保守。」
- **QPS 行（读）：** 「1 亿次浏览 ÷ 20,000 秒 = 5,000 次/秒。峰值按 3 倍：5,000 × 3 = 15,000 次/秒。」
- **QPS 行（写）：** 「1% 变成捐款：1 亿 × 1% = 100 万笔；100 万 ÷ 20,000 秒 = 50 笔/秒；峰值 × 3 = 150 笔/秒。」
- **读写比：** 「5,000 比 50 是 100 比 1，所以压力在活动页的读，不在捐款的写。」
- **写入行数：** 「每笔捐款大约写 5 行：建 Pending、改状态、写事件、写已应用记录、更新总额。150 × 5 = 750 行/秒，一个 Postgres 主库够，不需要分片。」
- **并发扣款：** 「每次调 PSP 约 0.5 秒，同时在飞的请求是 150 × 0.5 = 75 个。不大，所以并发不是瓶颈。」
- **存储：** 「每笔约 1 KB，100 万笔 = 1 GB 一天，一年约 365 GB，一台库放得下。」
- **爆红活动：** 「假设一个活动 1 万次浏览/秒，1% 转化就是 100 笔/秒打到同一个活动。热点在这个活动的总额和两个列表，不在整个系统。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 342">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">非功能需求 → 数字 → 逼出的设计</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">正确性：一次点击最多扣一次</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">没有「扣了款没记录」，总额不多算</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 重试键 · 先落库 · 总额只加一次</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">读：1 亿 ÷ 2 万秒 = 5,000/秒</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">峰值 ×3 = 15,000 次/秒</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 活动页读要走有界小结构 + 缓存</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">写：100 万 ÷ 2 万秒 = 50 笔/秒</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">峰值 ×3 = 150；约 750 行写/秒</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 一个 Postgres 主库够，不分片</text>
<rect x="8" y="236" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="256" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">并发扣款：150 × 0.5 秒 ≈ 75 个</text>
<text x="18" y="271" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">热门活动：1 万读/秒 → 100 笔/秒</text>
<text x="18" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 并发不是瓶颈；热点在总额和列表</text>
<text x="8" y="314" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每天 100 万笔 × 1 KB = 1 GB；一年 ≈ 365 GB</text>
<text x="8" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 亿次浏览 × 1% 转化 = 100 万笔（读写比 100:1）</text>
</svg>
白板上新增：四张便签，每张三行：需求、数字、它逼出的设计。深入问题从这四张里选。
**为什么这样说。** （约 4 分钟，累计第 9 分钟。）面试官看你的算术是不是对的，以及数字有没有变成设计决定。强的回答把总量、时间窗、除法一步步说出来：1 亿 ÷ 20,000 = 5,000，不是 2 万；然后说每个数字推出什么：读比写大 100 倍，所以优化读；750 行/秒，所以不分片。弱的回答是除错、不说时间窗从哪来，或者算出数字后不说它改变了什么。
**面试官可能接着问。**
- 20,000 秒是怎么来的？ → 这是我的假设：一天 86,400 秒，流量集中在白天，取约 5.5 小时的忙时窗口。您给我真实的日内分布，我就换掉；结论不变：读远大于写。
- 峰值为什么取 3 倍？ → 没有历史数据，3 倍是保守的经验值，我说出来：爆红和整点推送会集中。单个爆红活动我另外按 1 万次/秒算。
- 一年 365 GB 以后怎么办？ → 按月份对捐款表分区，旧分区转冷存储；它不是第一个瓶颈，我先不展开。
- 为什么说 750 行/秒不用分片？ → 都是按主键或唯一键的短事务，单主库在这个量级可以；我会预留余量并压测。真不够，再按 campaign_id 分库，因为总额只依赖同一个活动内的捐款。
**常见失分。**
- **除错数量级：** 1 亿 ÷ 20,000 是 5,000，说成 2 万，后面所有结论都偏 4 倍。
- **只说空话：** 「要高可用、高并发」没有数字，面试官无法判断你要的是什么系统。
- **算了不用：** 算出 100 比 1 的读写比却没说它让设计优化读，估算就成了表演。
- **漏掉正确性：** 这类系统最贵的事故是重复扣款和总额算错，不提它们，后面的机制就没有来由。
