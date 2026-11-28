---
id: bagu-like-leaderboard-5-windows
node: a.scenario.like-leaderboard
type: qa
step: 5
---
## Q
**日榜、周榜 · 时间窗口怎么设计**｜追问

面试官：「还要日榜、周榜，怎么设计？」

## A
**基本回答。** 按时间窗口分 key，如 `rank:day:20261104`，每个事件同时 `ZINCRBY` 到当天日榜，日榜设 TTL（保留 8 天，覆盖周榜用的 7 天），窗口靠 TTL 自然滚动，不用逐条删。周榜是最近 7 天日榜之和：`ZUNIONSTORE week 7 day1 ... day7 AGGREGATE SUM`，同一成员各日分数相加；合并是 O(N) 级重操作，所以定时预计算缓存，请求只读。只合并各日榜 Top N 是近似：每天都排在 N 名外但累计很高的对象会漏，精确要合并完整日榜。自然周可直接双写一个周榜 key，免去合并。午夜重置不能 `DEL` 再重建（重建前榜单为空），切换到新 key，新周期事件写新 key，旧榜保留一段时间后靠 TTL 过期。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每天一个 key，如 rank:day:20261104，设 TTL</text>
<rect x="8" y="24" width="40" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="28" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d1</text>
<line x1="28" y1="54" x2="28" y2="68" stroke-width="1.2" stroke="currentColor"/>
<rect x="54" y="24" width="40" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="74" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d2</text>
<line x1="74" y1="54" x2="74" y2="68" stroke-width="1.2" stroke="currentColor"/>
<rect x="100" y="24" width="40" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d3</text>
<line x1="120" y1="54" x2="120" y2="68" stroke-width="1.2" stroke="currentColor"/>
<rect x="146" y="24" width="40" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d4</text>
<line x1="166" y1="54" x2="166" y2="68" stroke-width="1.2" stroke="currentColor"/>
<rect x="192" y="24" width="40" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d5</text>
<line x1="212" y1="54" x2="212" y2="68" stroke-width="1.2" stroke="currentColor"/>
<rect x="238" y="24" width="40" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d6</text>
<line x1="258" y1="54" x2="258" y2="68" stroke-width="1.2" stroke="currentColor"/>
<rect x="284" y="24" width="40" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="304" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d7</text>
<line x1="304" y1="54" x2="304" y2="68" stroke-width="1.2" stroke="currentColor"/>
<line x1="28" y1="68" x2="304" y2="68" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="68" x2="170.0" y2="77.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,84 166.8,77.0 173.2,77.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="84" width="324" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ZUNIONSTORE week 7 … AGGREGATE SUM</text>
<line x1="170" y1="118" x2="170.0" y2="129.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,136 166.8,129.0 173.2,129.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="136" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="155" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">定时算好缓存，请求时直接读</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">午夜切换到新 key，不 DEL 重建</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口靠 TTL 自然滚动</text>
</svg>
七个日榜各自维护，加总（`SUM`）成周榜；周榜提前算好缓存，请求只读结果。
**举个例子。** 日榜 d1：a=5、b=1；d2：a=3、c=9。`ZUNIONSTORE week 2 d1 d2 AGGREGATE SUM` 得 a=8（5+3）、b=1、c=9，降序 c、a、b。周日 24 点按周编号建新 key，旧榜 TTL 过期前用户始终看到完整榜。
**容易错。**
- **日榜不设 TTL：** key 越积越多，内存一直涨。
