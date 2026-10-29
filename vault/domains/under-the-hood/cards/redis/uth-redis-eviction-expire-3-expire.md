---
id: uth-redis-eviction-expire-3-expire
node: redis.eviction-expire
type: qa
step: 3
---
## Q
**过期的键什么时候真正被删**｜Redis · 8.10

一百万个键都设了 TTL，Redis 是靠定时器到点逐个删除吗？

## A
**背景。** 给一百万个键设了过期时间（TTL）。最直观的办法是每个键一个定时器，到点就删；但要维护一百万个按到期时间排序的定时器，写入变贵。Redis 的办法：不追求准时，访问到才检查，再加后台随机抽查。

**结构。** 惰性删除加定期抽查，不给每个键设定时器。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">两条路: 惰性 + 定期抽查, 不给每个键设定时器</text>
<rect x="10" y="28" width="140" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="80" y="45.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">访问某个键时检查</text>
<line x1="150" y1="41" x2="176" y2="41" stroke="currentColor" stroke-width="1"/>
<polygon points="176,41 170.0,43.7 170.0,38.3" fill="currentColor"/>
<rect x="176" y="28" width="150" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="251" y="45.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已过期就当场删除</text>
<text x="8" y="78" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">定期: 每秒 10 次, 每个库随机抽 20 个带 TTL 的键</text>
<rect x="10" y="92" width="150" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="85" y="109.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">删掉抽到的过期键</text>
<line x1="160" y1="105" x2="190" y2="105" stroke="currentColor" stroke-width="1"/>
<polygon points="190,105 184.0,107.7 184.0,102.3" fill="currentColor"/>
<rect x="190" y="92" width="136" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="258" y="109.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过期的超过 10%?</text>
<line x1="258" y1="118" x2="258" y2="136" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="258,136 255.3,130.0 260.7,130.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="266" y="132" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<rect x="190" y="136" width="136" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="258" y="151.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">同一个库再抽一轮</text>
<text x="8" y="184" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">总耗时最多占约 25% 的 CPU; 从库不自己删, 等主库发 DEL</text>
<text x="8" y="202" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价: 过期键会暂时占着内存</text>
</svg>
```

**细节。**

- 惰性：访问某个键时检查，过期就当场删除
- 定期：每秒 10 次（`hz`），每个库随机抽 20 个带 TTL 的键，删掉过期的
- 抽样里过期的超过 10%，同一个库立刻再抽；总耗时最多占约 25% 的 CPU
- 从库不自己删，等主库发来 `DEL`

**为什么。** 精确删除要维护按到期时间排序的结构，写入更贵；抽样把清理摊到后台，代价是过期键会暂时占着内存。

**对应 LeetCode：** 无直接对应的题（过期与清理的取舍）
