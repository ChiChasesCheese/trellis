---
id: hi-fix-bounded-read-05-news-feed
node: fix.bounded-read
type: qa
step: 5
---
## Q
**News Feed 首页 · 有界读**｜补强

面试官：「用户打开首页要看到最新的 20 条，往下滑接着看。每次现算要去查几百个关注对象的帖子。怎么做？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **每个用户一个有界收件箱：** 「`feed:{uid}`，有序集合，成员是 post_id，分数是发帖时间的毫秒数，最多保留 200 条。」
- **发帖时写：** 「发帖后，fan-out worker 对每个粉丝 `ZADD feed:{uid} <毫秒> <post_id>`，再 `ZREMRANGEBYRANK feed:{uid} 0 -201`。」
- **读第一页：** 「`ZRANGE feed:{uid} 0 19 REV`，再 `MGET` 这 20 条帖子，帖子缓存里取。」
- **用游标翻页：** 「客户端带上一页最后一条的分数：`ZRANGE feed:{uid} (<分数> -inf BYSCORE REV LIMIT 0 20`。不用下标翻页：翻页途中有新帖插进来，下标整体后移，上一页最后一条会再出现一次。」
- **为什么是有序集合：** 「扇出任务会重试，`ZADD` 是幂等的；写入可能乱序，分数会把它放到正确的位置；还能按分数取游标。」
- **分数用毫秒时间戳：** 「分数是双精度浮点数，大于 2 的 53 次方的整数会丢精度，所以不用 64 位雪花 id；毫秒时间戳约 1.7 × 10^12，远小于它。同一毫秒的帖子极少，游标取包含式，客户端按 post_id 去重。」
- **粉丝极多的账号：** 「不写进每个粉丝的收件箱；读时再取这些账号自己的最近帖子 `ZRANGE posts:{celeb} 0 19 REV`，和收件箱按分数归并。读的条数也是有界的。」
- **容量：** 「按每条约 50 字节估算（假设），2 亿 × 200 × 50 B = 2 TB，按 user_id 分片放进集群；只给活跃用户维护收件箱，不活跃的回来时现算一次再写入。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写：发帖时扇出</text>
<rect x="8" y="26" width="324" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发帖 → 队列 → fan-out worker</text>
<rect x="8" y="90" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="110" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每个粉丝：feed:{uid}</text>
<text x="18" y="125" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZADD feed:{uid} &lt;发帖毫秒&gt; &lt;post_id&gt;</text>
<text x="18" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREMRANGEBYRANK feed:{uid} 0 -201</text>
<polyline points="170,62 170,90" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,90 166.8,83.0 173.2,83.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读：游标翻页</text>
<rect x="8" y="190" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="209.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">第 1 页：ZRANGE feed:{uid} 0 19 REV</text>
<text x="18" y="224.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">下一页：ZRANGE feed:{uid} (&lt;上页最后分数&gt;</text>
<text x="18" y="239.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">  -inf BYSCORE REV LIMIT 0 20</text>
<text x="18" y="254.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再 MGET 这 20 条帖子</text>
</svg>
白板上：发帖时扇出到每个粉丝的有界集合，读时用游标取一页。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 204">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">为什么不用下标翻页</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">下标：LRANGE 20 39</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">翻页途中有新帖进来，下标整体后移，</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上一页最后一条又出现一次</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">游标：(分数 -inf BYSCORE</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从「上一条的分数」往后取，</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新帖插在前面，不影响后面</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分数用毫秒时间戳：double 只能精确</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">表示到 2^53，64 位 id 会丢精度</text>
</svg>
白板上：游标比下标稳定，分数用毫秒时间戳。

**为什么这样说。** 面试官在看你把「首页」变成了哪个固定大小的读。弱的回答是每次读时对关注列表做归并；强的回答给出收件箱的结构、上限、写入命令、翻页命令，并说明明星账号走读时合并。
**面试官可能接着问。**
- 收件箱只有 200 条，用户滑到底了怎么办？ → 超出的部分走读时查询（按关注对象取更早的帖子）；很少有人滑到 200 条之后。
- 帖子被编辑或删除呢？ → 收件箱只存 id，帖子内容在缓存里；编辑只失效缓存，删除时读时过滤掉已删除的 id。
- 用户新关注了某人怎么办？ → 把对方最近的几条帖子补写进收件箱，或者下一次读时合并。
- 收件箱丢了怎么办？ → 它是缓存，用读聚合现算一次再写回。
**常见失分。**
- **用下标翻页：** 翻页途中重复或漏掉。
- **不说上限：** 收件箱无限增长。
- **收件箱里存完整内容：** 编辑和删除要改几百万份。
- **64 位 id 当分数：** 浮点精度丢失，顺序错乱。
