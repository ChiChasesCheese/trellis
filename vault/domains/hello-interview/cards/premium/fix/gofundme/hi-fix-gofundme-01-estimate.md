---
id: hi-fix-gofundme-01-estimate
node: fix.gofundme
type: qa
step: 1
---
## Q
**GoFundMe · 第 06:50 分 · 估算**｜复盘

面试官：「先估一下量：这个页面一秒钟大概有多少读、多少写？」

你会怎么回答？

## A
**当时的回答。**
- **取的数：** 你取了 1 亿次读取，按 20,000 秒摊开。
- **说出口的结果：** 你说每秒 2 万次读取；而 1 亿 ÷ 20,000 的结果是每秒 5,000 次。
- **后面用到它：** 「读多写少、要缓存」的判断都建在这个数上。
**差在哪。**
- **数和算式对不上：** 面试官听到 2 万，看到 5,000，分不清哪个才是你的假设。
- **错得有方向：** 偏大 4 倍，会让缓存和分片显得「非加不可」，面试官要回头重新核对每个依赖它的结论。
- **只有一个总数：** 没有拆读写，也没有平均和峰值，数字就推不出设计决定。
**应该这样说。**
- **先写单位：** 「1 亿次读取 ÷ 20,000 秒 = 每秒 5,000 次读取。」
- **回算一遍：** 「验一下：1e8 ÷ 2e4 = 0.5e4，是 5,000，不是 2 万。」
- **再拆读写：** 「我假设 1% 的访客会捐款：1 亿 × 1% = 100 万笔，÷ 20,000 = 每秒 50 笔写。读写比 100 比 1。」
- **再乘峰值：** 「峰值我取平均的 3 倍：读每秒 15,000，写每秒 150。」
- **说它改变什么：** 「读每秒几千，缓存挡掉；写每秒一百多，一台主库够。真正要设计的是一个爆红的活动，它把读集中到同一个键上。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 324">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">估算：总量 ÷ 时间，先写单位再回算</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 总量 ÷ 时间</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 亿次读 ÷ 20,000 秒</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 5,000 次/秒（不是 2 万）</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 用量级回算</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1e8 ÷ 2e4 = 0.5e4 = 5e3</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">差 4 倍马上看得出</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 读写分开（我的假设）</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1% 的访客捐款：50 笔/秒</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读 5,000/秒 · 写 50/秒 = 100 : 1</text>
<rect x="8" y="236" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="256" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">④ 再乘峰值 ×3（假设）</text>
<text x="18" y="271" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读 15,000/秒 · 写 150/秒</text>
<text x="18" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读走缓存；写一台主库够</text>
<text x="8" y="314" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">难点不在平均值，在某一个爆红的活动</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 174">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个总量，时间窗不同，速率不同</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">1 亿 ÷ 86,400 秒（全天）</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">≈ 1,157 次/秒</text>
<rect x="8" y="82" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="101.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">1 亿 ÷ 20,000 秒（约 5.6 小时）</text>
<text x="18" y="116.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 5,000 次/秒</text>
<text x="8" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先问清或先说出：流量集中在哪段时间。</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口越短，速率越高；我选哪个就说哪个。</text>
</svg>
白板上：四步估算和时间窗对比；每个假设都写出来，随时可以改。
**面试官可能接着问。**
- 为什么按 20,000 秒？ → 这是我的假设：流量集中在约 5.6 小时里（20,000 ÷ 3,600 ≈ 5.6）。按全天算是 1 亿 ÷ 86,400 ≈ 1,157 次/秒；我取窗口短、数字大的那个，设计留余量。
- 1% 的转化率哪来的？ → 我的假设，您给别的数我就改。结论对 0.1%（每秒 5 笔）和 5%（每秒 250 笔）一样：写都在单库量级。
- 峰值为什么是 3 倍？ → 没有历史数据，所以说成假设。爆红活动会把一个活动的读推得更高，所以我另外按「单个活动」设计热点。
**同类题。**
- **Ticketmaster：** 总人数 ÷ 开售窗口得到每秒请求，再看是不是瞬时尖峰。
- **Ad Click Aggregator：** 每天点击总数 ÷ 86,400，再乘峰值系数。
- **YouTube Top K、FB Live Comments：** 总事件数 ÷ 时间窗，先写单位再回算。
