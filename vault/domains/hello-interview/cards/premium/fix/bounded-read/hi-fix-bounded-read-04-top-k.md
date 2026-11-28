---
id: hi-fix-bounded-read-04-top-k
node: fix.bounded-read
type: qa
step: 4
---
## Q
**YouTube 热门视频榜 · 有界读**｜补强

面试官：「要显示最近一小时播放量最高的 100 个视频，每秒几十万个播放事件。榜单的有序集合怎么保持很小，又不丢计数？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先确认窗口和精度：** 「窗口是按小时滚动，还是滑动的最近一小时？要精确，还是近似就行？我先按滚动窗口、近似来讲，滑动窗口之后再谈。」
- **计数放在榜外面：** 「每个窗口一个 Count-Min Sketch：`CMS.INCRBY cms:{窗口} <video> 1`，返回这个视频当前的估计计数 c。」
- **榜里只放候选：** 「`ZADD topk:{窗口} <c> <video>`，写的是计数结构给出的绝对值，然后 `ZREMRANGEBYRANK topk:{窗口} 0 -1001`，留 1000 个候选。读的时候 `ZRANGE topk:{窗口} 0 99 REV WITHSCORES`，只取前 100。」
- **为什么不能 ZINCRBY：** 「被裁掉的视频再被 `ZINCRBY` 会从 0 起算。一个真实有 4 次的视频被裁出去，再来一次播放，榜里变成 1，而不是 5。」
- **下限优化：** 「消费者在内存里记着第 1000 名的分数 m；c 小于 m 的视频不必 `ZADD`，绝大多数事件因此不写榜。」
- **为什么留 1000 而不是 100：** 「留一点余量，让正在上升的视频有机会进来；读只取前 100。」
- **窗口怎么过期：** 「每个窗口的键设 `EXPIRE`，窗口结束后一段时间自动清掉。」
- **近似的代价：** 「Count-Min Sketch 只会高估，不会低估；我会向面试官说明这个误差，并问能不能接受。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 326">
<rect x="8" y="8" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="27.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">播放事件（每秒几十万）</text>
<text x="18" y="42.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个事件算一次计数</text>
<rect x="8" y="90" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="109.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">计数：CMS.INCRBY cms:{窗口} 视频 1</text>
<text x="18" y="124.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回这个视频的估计总数 c</text>
<rect x="8" y="172" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="192" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">候选集合 topk:{窗口}</text>
<text x="18" y="207" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c ≥ 第 1000 名才 ZADD topk c 视频</text>
<text x="18" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZREMRANGEBYRANK topk 0 -1001</text>
<rect x="8" y="270" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="289.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">读：ZRANGE topk 0 99 REV WITHSCORES</text>
<text x="18" y="304.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">固定 100 条</text>
<polyline points="170,54 170,90" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,90 166.8,83.0 173.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="170,136 170,172" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,172 166.8,165.0 173.2,165.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">绝对值 c</text>
<polyline points="170,234 170,270" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,270 166.8,263.0 173.2,263.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>
白板上：全量计数在 CMS 里，有序集合只收候选的绝对值。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 156">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">视频 v 真实有 4 次，被裁出候选</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">ZINCRBY topk 1 v</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v 不在集合里，从 0 起算：得到 1，错</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">ZADD topk 5 v</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写的是计数结构给出的绝对值 5，对</text>
<text x="8" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">计数放在榜外面，榜只收候选的绝对值</text>
</svg>
白板上：被裁出榜的视频用 ZINCRBY 会丢掉计数。

**为什么这样说。** 面试官在看你是否理解：有界的结构不能同时当计数器。弱的回答是「每个视频一个 `ZINCRBY`，再取前 K」：集合要么无限增长，要么一裁剪就丢计数。强的回答把计数和榜分开，榜只接收绝对值。
**面试官可能接着问。**
- 事件重放会让计数偏高吗？ → 会：近似场景可以接受；需要精确时在上游给每个事件一个 id，用已应用记录去重，那是另一个模式。
- Redis 丢了怎么办？ → 当前窗口的事件从 Kafka 重放重建；窗口越短，重放量越小。
- 滑动的最近一小时呢？ → 每分钟一个桶，查询时合并最近 60 个桶；这是近似的，我会先和面试官确认可以接受。
- 不用 CMS，直接用精确计数行不行？ → 视频数量有限时可以用 Redis 的哈希；基数极大时，CMS 的内存是固定的。
**常见失分。**
- **一个视频一个 ZINCRBY：** 被裁掉后计数从 0 起算，或者集合无限增长。
- **查询时才聚合：** 几十万事件每秒，没有预计算不可能在几十毫秒内读出前 100。
- **不先问精确还是近似：** 这个选择决定整套架构。
- **榜留得和 K 一样大：** 没有余量，边缘上的视频进不来。
