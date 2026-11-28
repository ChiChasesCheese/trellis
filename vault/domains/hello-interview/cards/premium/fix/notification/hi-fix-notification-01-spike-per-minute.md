---
id: hi-fix-notification-01-spike-per-minute
node: fix.notification
type: qa
step: 1
---
## Q
**通知系统 · 5M/分钟的尖峰**｜复盘

面试官：「营销活动的尖峰是每分钟 500 万条。换算成每秒是多少？日均每秒是多少？这个数说明哪一块最吃紧？」

你会怎么回答？

## A
**当时的回答。**
- **先把天当成月：** 你写 86,400 再乘 30，算出每秒的数（04:09）；面试官提醒「给你的是每天，不是每月」。
- **尖峰低了约 8 倍：** 5M 每分钟，你说「it's roughly about 10K right」（06:30），又改口「or are 100K sorry」（06:35）；正确是约 83,000 每秒，第一个数低了 8 倍。
- **比例前后不一：** 你口头说「20 times」，白板上写「200:1」，而正确的是约 14:1。
- **每个错都等到提醒才改：** 面试官发了两次提示，你才回到每分钟除以 60。
**差在哪。**
- **单位在脑子里，没在白板上：** 数字旁边没写「每分钟」「每秒」，每分钟和每秒的数混在一起，错了也看不出。
- **错的峰值推出错的设计：** 峰值 10K 每秒单库就扛得住，不需要日志；83K 每秒才是「库扛不住」的理由。设计要靠这个数撑着。
- **没有回算：** 乘回去只要 5 秒，面试官看不到你在检查自己。
**应该这样说。**
- **尖峰：** 「5,000,000 条/分钟 ÷ 60 秒/分钟 ≈ 83,000 条/秒。」
- **平均：** 「500,000,000 条/天 ÷ 86,400 秒/天 ≈ 5,800 条/秒。」
- **比：** 「83,000 ÷ 5,800 ≈ 14 比 1：尖峰是平均的 14 倍。」
- **回算：** 「83,000 × 60 ≈ 5,000,000 条/分钟，对得上。」
- **常识检查：** 「5M/分钟 持续 100 分钟就是一整天的 5 亿条，所以尖峰只会持续几分钟：10,000,000 条的活动约 120 秒发完。」
- **推出设计：** 「平均 5,800 写/秒一个库就够；尖峰 83,000 写/秒超过单库约 20,000 写/秒的舒适区，所以请求前面放一个日志（log）吸收尖峰。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先写时间基准：每分钟、每天，再到每秒</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">尖峰（条/秒）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5,000,000 条/分钟 ÷ 60 秒/分钟</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≈ 83,000 条/秒</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">平均（条/秒）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">500,000,000 条/天 ÷ 86,400 秒/天</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≈ 5,800 条/秒</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">尖峰 ÷ 平均（比）</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">83,000 ÷ 5,800 ≈ 14 : 1</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">当时白板：200 : 1（差 14 倍）</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 219">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回算，然后说这个数改变了什么设计</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">回算（条/分钟）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">83,000 条/秒 × 60 秒/分钟 ≈ 5,000,000</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对得上，才往下写</text>
<rect x="8" y="93" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">决定</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">尖峰 83,000 写/秒 &gt; 单库约 20,000 写/秒</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">平均 5,800 写/秒单库没问题</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 前面放日志吸收尖峰</text>
<text x="8" y="197" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10,000,000 条的活动 ÷ 83,000 条/秒 ≈ 120 秒</text>
<text x="8" y="213" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">尖峰是几分钟，不是一整天</text>
</svg>
白板上：三行带单位的算式，后面一行回算，最后一行是设计决定。
**为什么这样说。** （约 1 分钟。）面试官要看到两件事：数能被检查（每行带单位，回算一遍），数改变了设计（尖峰 83K 每秒所以要日志）。强的回答每一行都能被别人用笔核对；弱的回答报一个数，等面试官说「你再看看」。
**面试官可能接着问。**
- 每月 100,000,000 活跃用户，人均每天几条？ → 500,000,000 ÷ 100,000,000 = 5 条/人/天；这是用来核对给定数字，不是用来推峰值的。
- 峰值为什么不直接取平均的 3 倍？ → 3 倍是一般流量的经验值；这里面试官给了尖峰，直接用 83,000，不再乘。
- 尖峰持续多久，决定什么？ → 决定日志要吸收多少：按库每秒写 20,000 算，每秒积压 63,000，120 秒约 7,600,000 条，库要约 9 分钟排空。
**常见失分。**
- **数不带单位：** 「10K」是每秒还是每分钟，没人知道。
- **换算后不回算：** 一个零的错误在白板上留到结束。
- **只报数字不说设计：** 面试官会问「所以呢？」。
**同类题。**
- **任何给了「每分钟」「每小时」的题：** 先统一到每秒；小时除以 3,600，分钟除以 60，天除以 86,400。
- **Airbnb Wallet 的估算：** 同样是写单位、回算，见「带单位的估算」。
