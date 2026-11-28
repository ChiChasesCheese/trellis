---
id: bagu-penetration-4-avalanche
node: a.cache.penetration
type: qa
step: 3
---
## Q
**缓存雪崩 · 两类成因与防线**｜必会

面试官：「凌晨批量预热的缓存一起过期，或者 Redis 整个挂了，请求全压向数据库。怎么防？TTL 加随机、多级缓存各在什么情况下不够？」

## A
**基本回答。** 缓存雪崩（Cache Avalanche）有两类成因：大批 key 同时过期；Redis 整体宕机。前者给 TTL 加随机抖动，后者靠多级缓存（本地缓存容量小，冷启动的新实例也挡不住）、高可用（主从加哨兵或 Cluster，跨机架，发布扩容前先预热）、限流熔断降级保护数据库：数据库能承受多少 QPS 就只放行多少，其余返回默认值或稍旧的数据。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同时过期</text>
<text x="182" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">TTL 加随机</text>
<line x1="8" y1="150" x2="160" y2="150" stroke-width="1.2" stroke="currentColor"/>
<line x1="182" y1="150" x2="332" y2="150" stroke-width="1.2" stroke="currentColor"/>
<rect x="70" y="36" width="26" height="114" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">尖峰</text>
<rect x="190" y="116" width="20" height="34" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="110" width="20" height="40" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="246" y="120" width="20" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="274" y="112" width="20" height="38" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="302" y="118" width="20" height="32" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">过期时间 →</text>
<text x="182" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">过期时间 →</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ttl = base + random(0, base×20%)</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Redis 整体宕机抖动没用：要多级缓存、限流</text>
</svg>
左边所有 key 在同一时刻过期，数据库压力出现尖峰；右边加了随机抖动，过期点分散开，压力被摊平。
**容易错。**
- **以为 TTL 加随机能防宕机：** 它只打散过期点，Redis 整体不可用时没用，要多级缓存、高可用和限流。
- **以为本地缓存万能：** 容量小，冷启动的新实例也挡不住。
- **Redis 一恢复就放全量：** 冷缓存会再次被打穿，要慢速预热、逐步放量。
- **把雪崩当成击穿：** 击穿是一个热 key，雪崩是大批 key 或整个缓存。
**举个例子。** 1 万个榜单 key 02:00 一起写入，TTL 都是 3600 秒，03:00 同时过期，数据库出现尖峰。改成 3600 加随机 0 到 720 秒（base 的 20%），过期点散在 03:00 到 03:12。Redis 挂了抖动没用，本地缓存先挡一部分，限流只放行数据库能承受的 QPS，其余返回降级的旧榜。
