---
id: hi-fix-component-cost-06-ad-click-stream
node: fix.component-cost
type: qa
step: 6
---
## Q
**Ad Click Aggregator · 加组件：队列和流处理**｜补强

面试官：「点击量很大。你怎么算每个广告每分钟的点击数，而且结果要准？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **算量：** 「假设每天 10 亿次点击：1e9 ÷ 86,400 ≈ 11,574，约每秒 1.2 万；峰值取 3 倍，约 3.5 万。」
- **为什么不直接写库：** 「每次点击写一行，峰值每秒 3.5 万次，热门广告的聚合行还要排队更新。」
- **职责：** 「我加分区队列吸收峰值，聚合器按批累加，每批只写一次库。批大小 100，每秒 3.5 万 ÷ 100 = 350 次写。」
- **新问题：** 「队列至少一次：重平衡或重启会把同一批重发，点击会被重复计数；还有乱序和迟到。」
- **处理：** 「已应用的位置记在结果库里：每个分区一个 applied offset，和累加在同一个事务里更新；重发的批，offset 不超过 applied 就跳过。迟到的点击用事件时间和水位线：水位线之后才关窗，更晚的进单独的修正流。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 314">
<rect x="16" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分区 P3</text>
<text x="60" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Kafka</text>
<rect x="126" y="8" width="88" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">聚合器</text>
<rect x="236" y="8" width="88" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结果库</text>
<text x="64" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一批：offset 100–199</text>
<polyline points="60,84 170,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读 applied[P3] = 99</text>
<polyline points="170,118 280,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,118 273.0,121.2 273.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="276" y="140" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">累加 + applied[P3] = 199</text>
<polyline points="170,152 280,152" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,152 273.0,155.2 273.0,148.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="240.6" y="166" width="78.8" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一个事务</text>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重平衡 · 同一批重发</text>
<text x="64" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一批：offset 100–199</text>
<polyline points="60,242 170,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,242 163.0,245.2 163.0,238.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="174" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读 applied[P3] = 199</text>
<polyline points="170,276 280,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280,276 273.0,279.2 273.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="302" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已应用：跳过这一批</text>
<line x1="60" y1="48" x2="60" y2="291" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="306" x2="60" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="144" x2="170" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="212" x2="170" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="234" x2="170" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="48" x2="280" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="110" x2="280" y2="164" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="188" x2="280" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="280" y1="268" x2="280" y2="310" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="204" x2="101.72" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="238.28" y1="204" x2="332" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我要写在组件旁边的四行</text>
<rect x="8" y="26" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">加：队列和流处理，吸收点击</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">为了：1.2 万/秒、峰值 3.5 万/秒不压垮库</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新问题：重发、乱序、迟到</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">处理：offset 随结果提交；水位线收迟到</text>
</svg>
白板上：分区队列、聚合器、结果库；重发的那一批在 applied offset 上被跳过。
**为什么这样说。** （约 1 分钟。）面试官看你能不能把「精确一次」讲成一个具体的记录。强的回答说出 applied 是每个分区一个数，而不是每条点击一个键。弱的回答是「用 Flink 就是精确一次」。
**面试官可能接着问。**
- 为什么不给每条点击存一个去重键？ → 每秒 3.5 万个键写入太贵，而且键要一直存下去。一个分区一个 offset，成本是常数。
- 精确一次是框架自带的吗？ → 框架提供检查点和事务，原理一样：输出和位置一起提交。我讲原理，不依赖名词。
- 太晚到的点击？ → 水位线之后到的进修正流，按小时批量重算，并且在对外报表里标注数据还会修正。
**常见失分。**
- **把框架名当机制：** 面试官问记录在哪，答不出。
- **每条点击一个去重键：** 存储无限增长。
- **不说迟到：** 乱序和迟到是流处理必问的。
