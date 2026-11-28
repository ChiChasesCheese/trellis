---
id: hi-fix-bounded-read-06-live-comments
node: fix.bounded-read
type: qa
step: 6
---
## Q
**FB 直播评论 · 有界读**｜补强

面试官：「一场大型直播开始的瞬间，几百万人同时进来，每个人先要看到最近的评论。如果都打在评论库上会怎样？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先算一下：** 「一百万人在 60 秒内进来，是每秒约 16,667 次。每个人要的是同一个答案：这场直播最近的评论。」
- **一个有界结构：** 「`live:{video}:recent`，有序集合，成员是 comment_id，分数是评论时间的毫秒数。写评论成功时 `ZADD`，再 `ZREMRANGEBYRANK live:{video}:recent 0 -101`，留 100 条。」
- **新观众读什么：** 「`ZRANGE live:{video}:recent 0 49 REV` 取最新 50 个 id，再 `MGET comment:{id}` 取内容。评论库完全不参与。」
- **进场顺序：** 「先订阅实时流（SSE）并把新评论缓冲起来，再读最近 50 条，客户端按 comment_id 合并去重。先读后订阅，会漏掉中间到达的评论。」
- **更早的历史：** 「往上滑才查评论库，用游标分页：`commentId < :cursor`，每页固定条数。」
- **同一份答案再缓存一层：** 「16,667 次每秒、每次 50 条、每条约 200 字节，是约 167 MB 每秒，从同一个键读，网卡先吃紧。每个 API 实例把这份结果本地缓存 1 秒，一个实例每秒最多读 Redis 一次。」
- **删除评论：** 「审核删除就是 `ZREM live:{video}:recent <comment_id>`，成员是 id，所以好删。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 330">
<rect x="8" y="8" width="324" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">几百万观众同时进入</text>
<rect x="8" y="76" width="324" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="93" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">API 实例</text>
<text x="18" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">本地缓存最近 50 条，1 秒</text>
<text x="18" y="123" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个实例每秒最多读 Redis 一次</text>
<rect x="8" y="164" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Redis live:{video}:recent</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZADD … &lt;评论毫秒&gt; &lt;comment_id&gt;</text>
<text x="18" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREMRANGEBYRANK … 0 -101</text>
<text x="18" y="228.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">评论摘要在 comment:{id}，MGET</text>
<path d="M80,278 a90,6 0 0 1 180,0 v36 a90,6 0 0 1 -180,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M80,278 a90,6 0 0 0 180,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="170" y="295.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">评论库</text>
<text x="170" y="310.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有往上滑才查</text>
<polyline points="170,44 170,76" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,76 166.8,69.0 173.2,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="170,132 170,164" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,164 166.8,157.0 173.2,157.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZRANGE 0 49 REV</text>
<polyline points="170,240 170,272" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,272 166.8,265.0 173.2,265.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
白板上：观众先读 API 的本地缓存，缓存读固定大小的有序集合，评论库只在往上滑时才查。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">进场三步</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">① 先订阅实时流（SSE）</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新评论先放在缓冲里</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">② 再读最近 50 条</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一次有界读，不碰评论库</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">③ 按 comment_id 合并去重</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">补上空档，去掉重叠</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先读后订阅会漏掉中间到达的评论</text>
</svg>
白板上：进场三步，先订阅，再读，再按 id 合并。

**为什么这样说。** 面试官在看你有没有识别出：进场的读是同一个答案。弱的回答是「评论库读多，加读副本」；强的回答把最近的评论变成一个固定大小的结构，再加一层短时间的本地缓存，并说明订阅与读取的先后顺序。
**面试官可能接着问。**
- 为什么摘要不放在集合成员里？ → 放进去也可以，但删除要按完整内容 `ZREM`；成员只放 id，删除、编辑都只改一处。
- 评论的顺序怎么保证？ → 分数是评论时间的毫秒数；同一毫秒的并列由客户端按 comment_id 排序。
- 写评论每秒很多怎么办？ → 评论先进队列，由写入者按直播分区后写库和更新这个集合；这个集合只是最近的一个窗口。
- 有序集合丢了怎么办？ → 从评论库取最近 100 条重建；它是派生数据。
**常见失分。**
- **进场全打在评论库：** 每秒上万次相同的查询。
- **先读后订阅：** 漏掉两步之间的评论。
- **不说上限和本地缓存：** 同一个键被几万次每秒读取，网卡先扛不住。
- **用偏移量翻历史：** 评论不断插入，偏移量会重复或漏掉。
