---
id: bagu-like-leaderboard-1-design
node: a.scenario.like-leaderboard
type: qa
step: 1
---
## Q
**点赞计数与实时榜 · 整体设计**｜必会

面试官：「设计一个点赞计数和实时 Top 100 排行榜，你的整体方案是什么？」

## A
**基本回答。** 事件进 Redis 实时更新，数据库只做持久化、不承担实时排序。榜单用 ZSet：成员是作品或主播 ID，分数是点赞数；底层是跳表加 dict（按成员查分数 O(1)）。`ZINCRBY` 加分 O(log n)，成员不存在自动创建；`ZREVRANGE rank 0 99 WITHSCORES` 取前 100，O(log n + N)；`ZREVRANK` 查名次，O(log n)，从 0 开始，展示时加 1。同分按成员字典序（100 分的 a、b、c 降序取出是 c、b、a）；想先到先得要把时间编进分数，但分数是 double，只精确到 2^53（约 9×10^15），要留够位数。点赞和打赏事件同时写入消息队列，异步落库并对账；榜单分数是派生数据，Redis 丢了可由明细重建。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ZSet：成员 = 对象 ID，分数 = 点赞数</text>
<rect x="8" y="24" width="176" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="96" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">名次 0    d    150</text>
<rect x="8" y="54" width="176" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">名次 1    a    120</text>
<rect x="8" y="84" width="176" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">名次 2    c    100</text>
<rect x="8" y="114" width="176" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="131" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">名次 3    b    100</text>
<text x="196" y="42" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ZINCRBY 加分</text>
<text x="196" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ZREVRANGE 0 99</text>
<text x="196" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">取前 100 名</text>
<text x="196" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ZREVRANK 查名次</text>
<text x="196" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从 0 开始计</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">更新 O(log n)，取前 N 个 O(log n + N)</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同分按成员字典序：ZREVRANGE 先出 c 后出 b</text>
</svg>
左边是 ZSet 里已排好序的成员和分数，右边是三个常用命令各管什么。
**举个例子。** 新榜单 a、b、c 各 100 分：`ZREVRANGE rank 0 2` 返回 c、b、a；`ZINCRBY rank 5 a` 返回 105，再取榜是 a（105）、c、b；`ZREVRANK rank a` 为 0，`ZREVRANK rank b` 为 2。
**业务场景。** 直播间打赏榜每笔打赏 `ZINCRBY` 加分，客户端每几秒拉一次 `ZREVRANGE 0 99`，数据库只异步接收流水。
**容易错。**
- **以为榜单靠数据库排序：** 实时排序交给 ZSet。
- **把 Redis 当唯一数据源：** 榜单是派生视图，明细要落库。
