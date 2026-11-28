---
id: hi-fix-bounded-read-08-compare
node: fix.bounded-read
type: qa
step: 8
---
## Q
**有界读｜补强 · 跨题对照**

同一个模式放进六个页面字段：每个字段的结构是什么、上限多少、什么时候更新、读什么命令、丢了怎么重建？

## A
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 434">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个模式，六个页面字段</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GoFundMe 最近 / 最大</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZSET：成功时间 ≤100 · 金额 ≤10</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">成功且首次应用时写；缺了用 LIMIT 查询重建</text>
<rect x="8" y="94" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="114" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">游戏排行榜</text>
<text x="18" y="129" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZSET 全量，读有界：前 10 + 我 ±5</text>
<text x="18" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ZADD GT；从最高分表重建</text>
<rect x="8" y="162" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="182" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Top K 播放榜</text>
<text x="18" y="197" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZSET 候选 1000，读 100</text>
<text x="18" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">计数在 CMS，榜里 ZADD 绝对值</text>
<rect x="8" y="230" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="250" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">News Feed</text>
<text x="18" y="265" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每用户 ZSET ≤200，游标翻页</text>
<text x="18" y="280" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发帖时扇出；缺了现算一次</text>
<rect x="8" y="298" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="318" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">直播评论</text>
<text x="18" y="333" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每直播 ZSET ≤100，进场读 50</text>
<text x="18" y="348" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">API 本地缓存 1 秒；往上滑查库</text>
<rect x="8" y="366" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="386" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Ticketmaster 座位图</text>
<text x="18" y="401" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZSET：分数 = 到期时间</text>
<text x="18" y="416" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">占座成功时 ZADD；按分数读未来</text>
</svg>
白板上：六个页面字段，一行一个。

**同一套五问。** 页面上任何昂贵的字段，先答：
- **结构是什么：** 一个键，一种类型，说出名字。
- **上限多少：** 页面显示几条就留几条，或者场馆的座位总数；有时整个集合都留（排行榜），但读是有界的。
- **什么时候更新：** 事件成功之后，不是创建时，也不是每次读时。
- **读什么命令：** 说出完整的命令和范围。
- **丢了怎么重建：** 数据库仍是真相，重建是一次带索引的有界查询或扫描。

**为什么都是有序集合。** 更新由事件驱动，事件会重放、会乱序：`ZADD` 同成员同分数是幂等的，分数把乱序放回正确的位置，裁剪一条命令。列表只适合不会重放的场合。

**两个陷阱。**
- **计数不能放在被裁剪的集合里：** 被裁掉后再 `ZINCRBY` 会从 0 起算；计数放在榜外，榜里写绝对值。
- **分数是双精度浮点数：** 整数超过 2 的 53 次方会丢精度；用毫秒时间戳，不用 64 位 id。

**一句话版本。** 「每个昂贵的页面字段对应一个固定大小的有序集合，事件成功时 `ZADD` 再 `ZREMRANGEBYRANK` 裁到上限；页面只读这个集合，丢了就用带索引的查询重建。」
