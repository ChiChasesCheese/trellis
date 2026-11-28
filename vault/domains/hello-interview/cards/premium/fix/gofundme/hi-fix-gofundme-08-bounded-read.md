---
id: hi-fix-gofundme-08-bounded-read
node: fix.gofundme
type: qa
step: 8
---
## Q
**GoFundMe · 第 42:37 分 · 最近 100 笔与最大 10 笔**｜复盘

面试官：「活动页要展示最近的 100 笔捐款和最大的 10 笔。热门活动每秒被看上万次，不能每次都查主库。你怎么做？」

你会怎么回答？

## A
**当时的回答。**
- **去了写压力：** 你谈了分片、一致性哈希、给热门活动加盐、连接池和聚合。
**差在哪。**
- **没说页面读什么：** 这些手段分散的是写；页面每次打开，仍然要去搜索和排序捐款。
- **缺一个有界的对象：** 没有每个活动固定大小的结构，热门活动就一直在让数据库排序。
**应该这样说。**
- **先说读什么：** 「页面上每个贵的字段，对应一个小结构：总额是一个数，最近 100 笔和最大 10 笔各是一个有序集。」
- **最近 100 笔：** 「campaign:{id}:recent_donations 是有序集，按成功时间打分；成功时 ZADD 时间 id，再 ZREMRANGEBYRANK 0 -101，永远最多 100 个。读的时候 ZREVRANGE 0 99。不用列表：事件重放会把同一个 id 再推一次，或者把旧的捐款推到最前面；ZADD 同一个 id、同一个分数是幂等的。」
- **最大 10 笔：** 「campaign:{id}:largest_donations 是有序集，按金额打分；ZADD 之后 ZREMRANGEBYRANK 0 -11，只留分数最高的 10 个。」
- **页面请求：** 「GET /campaign/{id} 读这三个键，拿到不超过 110 个 id，再按主键批量取摘要；成本和捐款总数无关。」
- **何时刷新：** 「由处理 Completed 事件的工作进程更新。两个有序集的写都是幂等的，重放不会出错；Redis 丢了就按库重建。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 344">
<rect x="8" y="8" width="324" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">活动服务 · GET /campaigns/{id}</text>
<path d="M8,106 a107,6 0 0 1 214,0 v116 a107,6 0 0 1 -214,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M8,106 a107,6 0 0 0 214,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="115" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis（每个活动 3 个键）</text>
<rect x="16" y="140" width="198" height="24" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="115" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">total · 一个数</text>
<rect x="16" y="170" width="198" height="24" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">recent · 有序集，留 100 个</text>
<rect x="16" y="200" width="198" height="24" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="115" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">largest · 有序集，保留 10 个</text>
<path d="M240,106 a46,6 0 0 1 92,0 v116 a46,6 0 0 1 -92,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M240,106 a46,6 0 0 0 92,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="286" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="246" y="150" width="80" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="164.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">donations</text>
<text x="286" y="179.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主键</text>
<polyline points="80,48 80,100" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,100 76.8,93.0 83.2,93.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="86" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读 id</text>
<polyline points="286,48 286,100" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,100 282.8,93.0 289.2,93.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="280" y="80" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≤110 个</text>
<rect x="8" y="270" width="214" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="115" y="286.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工作进程</text>
<text x="115" y="301.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">处理 Completed 事件</text>
<polyline points="115,270 115,228" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="115,228 118.2,235.0 111.8,235.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="121" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">更新</text>
<text x="8" y="332" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">页面一次最多读：3 个 Redis 键 + 1 次主键批量查</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 275">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">页面字段 → 读哪个小结构 → 何时刷新</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">累计金额</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">total（一个数）</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">应用一次时 SET 成持久化值</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">最近 100 笔</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">recent：ZADD 成功时间 id，</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREMRANGEBYRANK 0 -101 只留 100 个</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">最大 10 笔</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">largest：ZADD 金额 id，</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREMRANGEBYRANK 0 -11 只留 10 个</text>
<text x="8" y="237" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个有序集的写都是幂等的：同一个 id、</text>
<text x="8" y="255" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个分数，重放多少次都一样；丢了就按库重建</text>
</svg>
白板上：页面读 Redis 里的三个键，再用主键批量取摘要；工作进程在成功事件上更新它们。
**面试官可能接着问。**
- 摘要从哪读？ → 按主键批量查 donations（110 个以内），或者成功时顺手把摘要放进 Redis 哈希；两种都是有界的。
- Redis 丢了怎么办？ → 按库重建：最近 100 笔取 status = Success、按完成时间倒序的前 100 行；最大 10 笔取按金额倒序的前 10 行。有索引时只读 100 行和 10 行。
- 分片还要不要？ → 写压力真大时才要，而且在这个结构之后：结构决定页面读什么，分片只决定这些结构放在哪台机器上。
**同类题。**
- **YouTube Top K、Leaderboard：** 排行榜的固定长度有序集。
- **News Feed：** 每个人最近 N 条的列表。
- **FB Live Comments：** 最近评论的有界窗口。
