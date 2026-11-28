---
id: hi-fix-bounded-read-07-ticketmaster
node: fix.bounded-read
type: qa
step: 7
---
## Q
**Ticketmaster 座位图 · 有界读**｜补强

面试官：「座位图要显示哪些座位正被别人临时占着（10 分钟）。如果你在 Redis 里用一个 Set 存被锁的座位，会有什么问题？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **Set 的毛病：** 「锁的键过期了，Set 里的成员不会跟着消失。每个放弃的结账都会留下一个永远显示「已占」的幽灵座位。」
- **用有序集合，分数是到期时间：** 「占座成功后 `ZADD event:{eid}:held <到期时间的秒数> <ticket_id>`。」
- **读：** 「还被占着的，就是分数在未来的：`ZRANGE event:{eid}:held (<now> +inf BYSCORE`。过期的自动不再出现，不需要谁来清理。」
- **清理只是整理：** 「读时或定时 `ZREMRANGEBYSCORE event:{eid}:held -inf <now>`，把已过期的成员删掉，保持集合小。」
- **提前释放：** 「用户取消或支付完成，直接 `ZREM`。」
- **座位图怎么拼：** 「已售的来自数据库，占用中的来自这个集合，合起来就是座位图。」
- **大小有界：** 「集合最多有场馆的座位总数那么多成员，比如两万个。」
- **判决仍在锁上：** 「这个集合只用来显示。占座的判决是 `SET lock NX EX`；集合和锁差一两秒，只影响显示，不影响正确性。」
- **读很多时：** 「座位图的结果在 API 或边缘缓存 1 到 2 秒，同一场演出所有观众共用。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">held:{event}  分数 = 到期时间</text>
<rect x="8" y="26" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">座位 s1   到期 10:00:20   已过期</text>
<rect x="8" y="60" width="324" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">座位 s2   到期 10:03:00   占用中</text>
<rect x="8" y="94" width="324" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">座位 s3   到期 10:07:30   占用中</text>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">now = 10:01:00</text>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读：ZRANGE held (now +inf BYSCORE</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只返回分数在未来的座位</text>
</svg>
白板上：分数是到期时间，读的时候只取分数在未来的成员。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">座位图 = 已售 ∪ 占用</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">已售</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">来自数据库 status = sold</text>
<rect x="8" y="90" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="110" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">占用中</text>
<text x="18" y="125" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZRANGE held (now +inf BYSCORE</text>
<text x="18" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上限 = 场馆座位总数</text>
<rect x="8" y="170" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="190" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">占座的判决不在这里</text>
<text x="18" y="205" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET lock NX EX：锁才是真相</text>
<text x="18" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">集合只用来显示，差一两秒无妨</text>
</svg>
白板上：座位图由已售和占用合成，判决仍在锁上。

**为什么这样说。** 面试官在看你有没有注意到：缓存里的结构也有生命周期。弱的回答是「用 Redis Set 存锁住的座位」，没想到成员不会过期；强的回答让分数就是到期时间，让读本身过滤掉过期的。
**面试官可能接着问。**
- 为什么不给每个成员单独设过期？ → Set 和有序集合的成员没有单独的 TTL；用分数加读时过滤，等价于每个成员一个 TTL。
- 服务器之间的时钟不一致呢？ → 显示可能差一两秒；判决由 Redis 的 TTL 做，集合只用来显示。
- 集合丢了怎么办？ → 扫描现存的锁键重建，或者让座位图暂时只显示已售，几秒后自动恢复。
- 多个座位一起占呢？ → 每个座位一个成员，同一个到期时间。
**常见失分。**
- **用 Set 存锁住的座位：** 过期的成员不会消失，幽灵座位。
- **用集合当判决：** 它和锁不同步时会出现重复占座。
- **不裁剪也不过滤：** 集合里积累着早已过期的成员。
- **每次读都去数据库：** 热门演出的座位图每秒几百万次。
