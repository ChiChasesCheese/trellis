---
id: bagu-multilevel-1-multi-level
node: b.cache.multilevel
type: qa
step: 1
---
## Q
**多级缓存 · 设计、TTL 与冷启动**｜追问

面试官：「热门商品详情读 QPS 极高，多级缓存怎么设计？各级怎么保证一致？新实例本地缓存是空的，怎么避免瞬间击穿？」

## A
**基本回答。** 读依次查浏览器或 CDN → 本地缓存（Caffeine）→ Redis → 数据库，回填时自下而上。本地缓存没有网络开销、不受 Redis 吞吐限制，能挡热 key；Redis 容量大、全实例共享，保护数据库。代价是一致性：本地缓存无法精确同步失效，靠短 TTL（几秒到一分钟）加广播失效，能容忍的不一致时长就是 TTL。写库后删 Redis，再用 Redis Pub/Sub 或 MQ 广播让各实例删本地缓存，广播可能丢，所以 TTL 是兜底。
**2026 亮点。** 本地层失效可交给服务端：开 Redis / Valkey 的 client tracking（RESP3 推送失效），key 被改、过期或淘汰时推送，比靠 TTL 猜更准，也省掉自建广播；代价是追踪表占内存，连接断开必须清空本地缓存，写频繁的 key 失效消息比命中收益还贵，部分官方客户端仍是实验性。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="10" y="8" width="120" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器 / CDN</text>
<text x="146" y="25" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Cache-Control</text>
<text x="146" y="41" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主动 purge</text>
<line x1="70" y1="48" x2="70" y2="62" stroke="currentColor" stroke-width="1.2"/>
<polygon points="70,62 67.0,55.7 73.0,55.7" fill="currentColor"/>
<rect x="10" y="62" width="120" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="70" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地 Caffeine</text>
<text x="146" y="79" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每实例几百 MB</text>
<text x="146" y="95" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">纳秒到微秒</text>
<line x1="70" y1="102" x2="70" y2="116" stroke="currentColor" stroke-width="1.2"/>
<polygon points="70,116 67.0,109.7 73.0,109.7" fill="currentColor"/>
<rect x="10" y="116" width="120" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="146" y="133" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">数十 GB 到 TB</text>
<text x="146" y="149" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">亚毫秒到毫秒</text>
<line x1="70" y1="156" x2="70" y2="170" stroke="currentColor" stroke-width="1.2"/>
<polygon points="70,170 67.0,163.7 73.0,163.7" fill="currentColor"/>
<rect x="10" y="170" width="120" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="146" y="187" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">权威数据</text>
<text x="146" y="203" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最终的真相</text>
<text x="10" y="238" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读：自上而下，未命中就问下一层</text>
<text x="10" y="256" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">回填：自下而上；本地失效靠短 TTL 兜底</text>
</svg>
从上到下一层比一层大、一层比一层慢；高亮的本地缓存是挡住热 key 的关键一层，也是一致性最难的一层。
**容易错。**
- **以为广播失效就够了：** 广播可能丢，TTL 才是兜底。
- **本地缓存不设上限：** 要设最大条目数或权重防 OOM，软引用并不可靠；Caffeine 用 W-TinyLFU，以计数草图（count-min sketch，小内存估算访问频率）判断谁留下，命中率比纯 LRU 高。
- **所有实例同时重启：** 全部本地缓存同时变空，冷启动一起冲击 Redis 和数据库；要启动时预热热点 key、分批滚动发布、限流，进程内用 `computeIfAbsent` 合并同一 key 的并发加载。
- **只看总命中率：** 要分层监控命中率和淘汰数，才知道是哪一层出了问题。
**举个例子。** 热门商品 1001 本地 TTL 10 秒：第一次读本地和 Redis 都没有，查库后回填两层，之后 10 秒内读都在本地命中。商家改价：写库、删 Redis、广播「删 1001」；某台实例丢了广播，最多再过 10 秒 TTL 到期就读到新价。
