---
id: bagu-idempotency-design-5-dedup-growth
node: a.idem.idempotency-design
type: qa
step: 5
---
## Q
**幂等 · 去重表会无限增长吗**｜追问

面试官：「去重表每天写入上千万行，会无限增长吗？保留多久？」

## A
**基本回答。** 会。按时间分区，保留期大于最大可能的重试窗口（如 7 天），到期整分区 DROP，几乎瞬间完成，不产生大量 undo 日志和 binlog。更稳的做法是业务键本身有唯一约束，不依赖去重表的保留期。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 124">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按天分区，到期整分区 DROP</text>
<rect x="8" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="26" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D-7</text>
<rect x="49" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="67" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D-6</text>
<rect x="90" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D-5</text>
<rect x="131" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="149" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D-4</text>
<rect x="172" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="190" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D-3</text>
<rect x="213" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="231" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D-2</text>
<rect x="254" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D-1</text>
<rect x="295" y="24" width="36" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="313" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">今天</text>
<line x1="49" y1="64" x2="332" y2="64" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="49" y1="60" x2="49" y2="68" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="332" y1="60" x2="332" y2="68" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="190" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保留 7 天，大于最大重试窗口</text>
<line x1="213" y1="96" x2="332" y2="96" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="213" y1="92" x2="213" y2="100" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="332" y1="92" x2="332" y2="100" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="332" y="116" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">渠道最多重试 3 天</text>
</svg>
每天一个分区，最左边虚线的是到期的旧分区，整个删掉；右边保留 7 天。重试最多发生在最近 3 天，所以 7 天的保留期覆盖了所有可能的重复，还留了余量。
**容易错。**
- **以为去重表可以永久保留：**每天上千万行，不清理就无限增长。
- **用大 DELETE 清理：**长时间持锁、拖慢主从复制，要分区 DROP 或分批删。
- **保留期随便设：**必须大于最大重试窗口，不然老的重复消息认不出来。
- **分库分表后还以为有本地事务：**去重表和业务表不同库时，要让去重键跟业务表同分片，或用 TCC、Saga。
**举个例子。** 每天写入 1000 万行去重记录，按天分区保留 7 天，稳态约 7000 万行；渠道最多回调 3 天，7 天大于 3 天，清理安全。反例：保留期只有 1 天而渠道第 2 天还会重试，这次重试认不出来，被当成新消息重复处理。
