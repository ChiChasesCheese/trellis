---
id: bagu-zset-skiplist-1-usage
node: a.redis.zset-skiplist
type: qa
step: 1
---
## Q
**ZSet · 常见用法与命令复杂度**｜必会

面试官：「打赏榜要取 Top 100 主播，还要查某个主播的实时名次。用 Redis 什么结构、哪些命令、复杂度各是多少？」

## A
**基本回答。** 用有序集合（ZSet）：每个成员带一个 double 分数，Redis 始终按分数排好序。每笔打赏 `ZINCRBY rank:day:20261104 <金额> <主播ID>` 累加（成员不存在从 0 开始）；Top 100 用 `ZREVRANGE key 0 99 WITHSCORES`（6.2 起推荐 `ZRANGE key 0 99 REV`）；名次用 `ZREVRANK`，下标从 0 数，展示要加 1。`ZADD`、`ZINCRBY`、`ZREM`、`ZRANK` 是 O(log N)，`ZRANGE` 是 O(log N + M)（先 O(log N) 定位，再顺链表走 M 步，所以榜里几十万成员取前 100 也不慢），`ZSCORE` 是 O(1)：底层除了跳表还有一张 dict 记「成员 → 分数」。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 186">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有序集合 rank:day:20261104</text>
<text x="14" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="26" y="28" width="134" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主播C  900</text>
<text x="14" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="26" y="60" width="134" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="93.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主播B  850</text>
<text x="14" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="26" y="92" width="134" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主播A  750</text>
<text x="14" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="26" y="124" width="134" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="141.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主播D  420</text>
<text x="26" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">…共 N 个成员，下标从 0 数</text>
<line x1="176" y1="41" x2="162" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="162.0,41.0 169.0,37.8 169.0,44.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="45" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREVRANGE 0 99</text>
<text x="180" y="60" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">取下标 0–99 的前 100 名</text>
<line x1="176" y1="73" x2="162" y2="73" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="162.0,73.0 169.0,69.8 169.0,76.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="180" y="77" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZINCRBY +400</text>
<text x="180" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ZREVRANK 主播B → 1</text>
<line x1="176" y1="137" x2="162" y2="137" stroke-width="1.2" stroke="currentColor"/>
<polygon points="162.0,137.0 169.0,133.8 169.0,140.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="141" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ZSCORE 主播D → 420</text>
<text x="180" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">O(1)，查哈希表</text>
</svg>
左边的数字是下标（0 就是第 1 名）；右边是命令：取前 100 名是定位到头部再顺着读，加分和查名次各走一条路径，查分数直接查哈希表。
**其他用法。**
- **延迟队列：** score 放到期时间戳，`ZRANGEBYSCORE key -inf <now> LIMIT 0 N` 取到期任务；多个消费者会取到同一个，所以要 `ZREM`，返回 1 的才执行，返回 0 说明被抢走。
- **滑动窗口限流：** score 放请求时间戳；先 `ZREMRANGEBYSCORE` 清窗口外的旧请求，再 `ZCARD` 数剩几个，没超限就 `ZADD` 当前请求。
**业务场景。** 榜单页要「Top 100 加我的名次」：一次 `ZREVRANGE` 加一次 `ZREVRANK`，几十万成员也在毫秒内返回；用 MySQL `ORDER BY SUM(amount)` 每次刷新都要聚合流水再排序，撑不住。
**容易错。**
- **ZRANGE 0 -1：** O(N)，榜单涨到几十万成员时一次调用就堵住单线程，榜单页永远带范围。
