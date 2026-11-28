---
id: hi-fix-bounded-read-01-mechanism
node: fix.bounded-read
type: qa
step: 1
---
## Q
**有界读 (Bounded Read)｜补强 · 机制**

活动页要显示「最近 100 笔捐款」「最大 10 笔」，排行榜要显示前 10 名。每次打开都去库里查会怎样？「有界读」是什么，面试时怎么把它说出口？

## A
**要防的失败。** 页面每次被打开，就去主库重新排序、取前 N 条、求和。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 334">
<rect x="8" y="8" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="27.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每次打开活动页（5,000 次/秒）</text>
<text x="18" y="42.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同样的三个问题，一遍又一遍</text>
<rect x="8" y="100" width="324" height="78" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">最近 100 笔：ORDER BY 时间 LIMIT 100</text>
<text x="18" y="143" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">最大 10 笔：ORDER BY 金额 LIMIT 10</text>
<text x="18" y="158" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">总额：SUM(金额)</text>
<path d="M80,230 a90,6 0 0 1 180,0 v44 a90,6 0 0 1 -180,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M80,230 a90,6 0 0 0 180,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="170" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款库 Postgres</text>
<text x="170" y="266.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还在承担所有写入</text>
<polyline points="170,54 170,100" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,100 166.8,93.0 173.2,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="176" y="82" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读</text>
<polyline points="170,178 170,224" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,224 166.8,217.0 173.2,217.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="176" y="206" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">× 3</text>
<text x="8" y="304" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有索引时单次很便宜，但答案几乎不变，</text>
<text x="8" y="322" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">却要在主库上每秒重算上万次</text>
</svg>
白板上：同样的三个问题，每秒被重复几千次，全压在同时承担写入的主库上。
- **答案几乎不变：** 有合适的索引，单次查询并不贵；贵的是同一个答案每秒被算几千次。
- **没有索引更糟：** 每次要对整个活动的捐款排序，热门活动的行数越多越慢。
- **分片治不了它：** 分片、一致性哈希、连接池，解决的是写入压力和连接数，没有回答「页面到底读什么」。

**机制。** 每个昂贵的页面字段，对应一个固定大小的小结构，在数据变化时顺手更新；页面只读这个小结构。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 322">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写：成功时更新，各自裁到上限</text>
<rect x="8" y="26" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="52" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">捐款转到 SUCCESS（只处理一次）</text>
<text x="18" y="67" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZADD recent &lt;成功时间&gt; &lt;id&gt;</text>
<text x="18" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREMRANGEBYRANK recent 0 -101</text>
<rect x="8" y="108" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="134" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同一个事件，另一个结构</text>
<text x="18" y="149" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZADD largest &lt;金额&gt; &lt;id&gt;</text>
<text x="18" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREMRANGEBYRANK largest 0 -11</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读：只读固定大小的结构</text>
<rect x="8" y="222" width="324" height="90" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="248.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /campaign/{id}</text>
<text x="18" y="263.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZRANGE recent 0 99 REV</text>
<text x="18" y="278.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZRANGE largest 0 9 REV WITHSCORES</text>
<text x="18" y="293.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再 MGET 这 ≤ 110 条的摘要</text>
</svg>
白板上：写的时候各自裁到上限，读的时候只读固定大小的结构。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">recent 集合（示意，只留 3 条）</text>
<rect x="8" y="26" width="200" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分数 1005   成员 d5</text>
<rect x="8" y="60" width="200" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分数 1004   成员 d4</text>
<rect x="8" y="94" width="200" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分数 1003   成员 d3</text>
<rect x="8" y="128" width="200" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分数 1002   成员 d2</text>
<rect x="8" y="162" width="200" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分数 1001   成员 d1</text>
<polyline points="220,40 220,108" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="220,108 216.8,101.0 223.2,101.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="228" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保留</text>
<text x="228" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被裁掉</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ZREMRANGEBYRANK key 0 -4：删掉</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从最小分数起、除了最后 3 个的全部</text>
</svg>
白板上：有序集合按分数排，裁剪就是删掉排在最后面的一段。
- **结构：** 一个字段一个键，`campaign:{id}:recent`、`campaign:{id}:largest`；成员是 id，摘要另存。
- **上限：** 页面显示几条，集合就留几条：最近 100、最大 10。
- **何时更新：** 捐款成功（且只处理一次）的那个事件，不在创建时，不在每次读时。
- **读什么命令：** `ZRANGE key 0 99 REV`；带分数的 `ZRANGE key 0 9 REV WITHSCORES`（等价于 `ZREVRANGE`）。
- **丢了怎么重建：** 数据库仍是真相；Redis 丢了，用带索引的 `ORDER BY … LIMIT N` 查询重建一次。
- **裁剪命令：** 保留分数最高的 N 个，就是 `ZREMRANGEBYRANK key 0 -(N+1)`：最小的排名是 0，删掉从 0 到倒数第 N+1 个。放进 `MULTI … EXEC` 里，读的人不会看到 N+1 条。

**为什么是有序集合，不是列表。** 更新是由事件驱动的，事件会重放、会乱序。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个事件重放时</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">列表 LPUSH + LTRIM</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再推一次：同一个 id 在榜里出现两次</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">列表，旧捐款重放</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧 id 被推到最前面，被裁掉的又回来</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">有序集合 ZADD</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同成员同分数：什么也没变</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">有序集合，旧捐款重放</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分数最小，立刻又被裁掉</text>
</svg>
白板上：列表做法在重放时出错，有序集合同成员同分数是幂等的。
- **朴素版是列表：** `LPUSH` 加 `LTRIM 0 99`，不重放时没问题。
- **重放就出错：** 同一个 id 被推两次；一笔旧捐款重放，会被推到最前面，已经被裁掉的又回来了。
- **有序集合不怕：** `ZADD` 同成员同分数什么也不改；旧的分数小，立刻又被裁掉。

**在面试里说这一句。** 「活动页的最近 100 笔，是一个按成功时间打分的有序集合，成功时 `ZADD` 再裁到 100；最大 10 笔同理，按金额打分裁到 10；页面只读这两个集合里的 id，再取这 110 条摘要。」

**怎么认出这类题。**
- **页面字段是「最近 N」「最大 N」「前 N 名」：** 面试官问「不查主库怎么显示」。
- **读多写少：** 同一个答案被很多人反复读。
- **你想说分片之前：** 先问自己「这个字段读的是哪个小东西」。

**常见失分。**
- **去讲分片和盐值：** 回答的是写入扩展，没有回答页面读什么。
- **不说上限：** 结构无限增长，等于把查询搬到 Redis 里。
- **用列表接重放的事件：** 重复和旧数据都会混进来。
