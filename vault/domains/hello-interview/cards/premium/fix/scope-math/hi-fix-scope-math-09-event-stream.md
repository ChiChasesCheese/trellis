---
id: hi-fix-scope-math-09-event-stream
node: fix.scope-math
type: qa
step: 9
---
## Q
**通知事件流 · 这回要不要分片**｜补强

面试官：「通知系统：50,000,000 用户，每人每天产生 20 条事件，每条 200 字节，保留 90 天。算一下，一个 Postgres 够吗？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **事件数：** 「50,000,000 用户 × 20 条/天 = 1,000,000,000 条/天。」
- **写速率：** 「1,000,000,000 条/天 ÷ 86,400 秒/天 ≈ 11,600 条/秒；峰值按 3 倍，约 35,000 条/秒。」
- **存储：** 「1,000,000,000 条/天 × 200 字节 = 200 GB/天；× 90 天 = 18,000 GB = 18 TB，索引之前。」
- **决定：** 「写 35,000 条/秒超过单主库简单写的舒适区（约 2 万次/秒），存储 18 TB 也比前两题大一个数量级。所以这回不是「一个 Postgres」：事件先进 Kafka 缓冲，批量写入按时间分区的追加存储，用户读按 user_id 分片。」
- **先问保留期：** 「存储由保留期决定。如果 7 天就够：200 GB/天 × 7 天 = 1.4 TB，存储回到单库的量级；写速率不变，仍然要批量写。」
- **说明这是同一套算法：** 「钱包和开票算出来是一个库，这题算出来不是；差别是数字，不是方法。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">通知事件流：每行带单位</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">事件数</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">50,000,000 用户 × 20 条/天 = 1,000,000,000 条/天</text>
<rect x="8" y="78" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">写速率</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1,000,000,000 ÷ 86,400 秒/天 ≈ 11,600 条/秒</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值 ×3 ≈ 35,000 条/秒</text>
<rect x="8" y="145" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">存储</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1,000,000,000 条/天 × 200 字节 = 200 GB/天</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">× 90 天 = 18 TB（索引之前）</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 164">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一套算法，这回数字改变了设计</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">写 35,000 条/秒</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">超过单主库简单写的舒适区（约 2 万/秒）</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">批量写，或按 user_id 分片</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">存储 18 TB</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">追加写的存储，按时间分区</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保留期是旋钮：7 天 = 1.4 TB</text>
</svg>
白板上：三行算式，两行决定，另有一行写保留期是旋钮。
**为什么这样说。** （约 1 分钟。）这张卡是前两题的对照：同样的算式，结论相反。强的回答说明是哪个数字推翻了「一个库」；弱的回答每道题的结论都是「分片」，或者每道题都是「不分片」，与数字无关。
**面试官可能接着问。**
- 为什么 20 条/天？ → 我的假设，包含系统消息和营销推送；给了别的数我就改，10 条/天：峰值约 17,000 条/秒、存储 9 TB，贴着单库舒适区上沿，仍要批量写、分区、缩短保留期；40 条/天：峰值约 70,000 条/秒，更明显超过。方向不变，只是超出的幅度不同。
- 保留期能不能不要 90 天？ → 先问需求：用户翻几天的通知？90 天是合规要求，还是随口说的？这是最便宜的旋钮。
- 分片键为什么是 user_id？ → 读都是「某个用户最近的通知」，同一个用户落在同一片，一次读一片。
**常见失分。**
- **每题都套同一个结论：** 数字不同，结论应该不同。
- **只算存储不算写速率：** 35,000 条/秒才是推翻单库的第一个数字。
- **不问保留期：** 少问一句，就多出 10 倍的存储。
