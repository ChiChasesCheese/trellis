---
id: hi-fix-scope-math-03-reads-writes-peak
node: fix.scope-math
type: qa
step: 3
---
## Q
**GoFundMe · 读写分开、再乘峰值**｜补强

面试官：「平均每秒 5,000 次读，你怎么拆读写？峰值又是多少？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先拆读写：** 「读每秒 5,000。我假设 1% 的访客会捐款：1 亿 × 1% = 100 万笔，÷ 20,000 秒 = 每秒 50 笔写。读写比 100 比 1。」
- **读写比决定先挡哪边：** 「差两个量级，所以先挡读：缓存和小结构；写每秒几十笔，不是第一个问题。」
- **再乘峰值：** 「峰值取平均的 3 倍：读 15,000，写 150。」
- **峰值系数是假设：** 「3 倍是我的假设，没有历史数据；您给别的数我就改。」
- **限时捐款的例子：** 「平均 386 笔/秒，活动开始和截止前集中，按 5 倍：386 × 5 ≈ 1,930，我取 2,000 笔/秒。」
- **再问最热的那一个：** 「假设 10% 的读落在最热的一个活动上：15,000 × 10% = 1,500 次/秒，打在同一个键上；这才是要单独设计的地方。」
- **按峰值设计，按平均算成本：** 「容量按峰值准备，存储和成本按平均和增长算。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读 vs 写，平均 vs 峰值（次/秒）</text>
<text x="8" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读·平均</text>
<rect x="76" y="32" width="66.6667" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="148.667" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5,000</text>
<text x="8" y="74" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读·峰值</text>
<rect x="76" y="62" width="200" height="16" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">15,000</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写·平均</text>
<rect x="76" y="92" width="2" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写·峰值</text>
<rect x="76" y="122" width="2" height="16" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="84" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">150</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读 : 写 = 5,000 : 50 = 100 : 1</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">假设：1% 访客捐款；峰值 = 平均 × 3</text>
<line x1="8" y1="196" x2="332" y2="196" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">限时捐款：386 × 5 ≈ 1,930，取 2,000 笔/秒</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单个热点：15,000 × 10% = 1,500 次/秒 / 键</text>
</svg>
白板上：四根条；写的条比读的条小两个量级，一眼看出先挡哪边。
**为什么这样说。** （约 1 分钟。）读写比、峰值和热点这三步，是把一个总数变成设计决定的桥。强的回答每一步都带一个假设和一个数，并且最后落到「所以要单独设计热点」。弱的回答只有一个平均数，或者只说「读多写少」，没有数。
**面试官可能接着问。**
- 写这么少，为什么还要提主库？ → 因为写是正确性的所在：每秒 150 笔单库没压力，但每一笔都要做到只扣一次、只加一次。规模小，不代表可以省正确性。
- 转化率换成 0.1% 或 5% 呢？ → 写变成每秒 5 或 250 笔，仍是单库量级；结论不变，所以我不在这个假设上花时间。
- 为什么按 3 倍，限时捐款按 5 倍？ → 因为限时活动更集中：开始和截止前都会冲高。系数是对形状的假设，我会说出理由。
**常见失分。**
- **只报平均：** 平均不压垮系统，峰值才会。
- **不拆读写：** 一个总数推不出该挡哪一边。
- **忘了热点：** 全局数字不大，单个键的数字可能很大。
