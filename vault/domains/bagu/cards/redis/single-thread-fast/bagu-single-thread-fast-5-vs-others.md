---
id: bagu-single-thread-fast-5-vs-others
node: a.redis.single-thread-fast
type: qa
step: 5
---
## Q
**选型 · 为什么命令执行不做多线程，和 Memcached、本地缓存怎么选**｜追问

面试官：「为什么不让命令执行也多线程？和 Memcached、Caffeine 这类本地缓存比，什么时候选 Redis？」

## A
**基本回答。** 命令执行不做多线程：瓶颈不是 CPU；多线程改同一份数据要加锁，还会削弱命令、事务、Lua 的原子性；想用多核就横向分片（多实例或 Cluster）。Memcached 只有简单字符串，Redis 有丰富结构、持久化、集群、Lua，所以多数场景选 Redis。本地缓存无网络、纳秒级，但容量受堆限制、各实例各一份、更新靠失效广播，适合极热且少变的数据。常见是两级：本地挡最热 key，Redis 做共享层（多一次网络往返），数据库兜底。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读请求先挡在最近的一层</text>
<rect x="8" y="26" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地缓存</text>
<text x="56" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Caffeine</text>
<rect x="122" y="26" width="96" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="170" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">共享层</text>
<rect x="236" y="26" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="284" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">权威</text>
<line x1="104" y1="48" x2="122" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,48 115.0,51.2 115.0,44.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="218" y1="48" x2="236" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236,48 229.0,51.2 229.0,44.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="56" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无网络，纳秒级</text>
<text x="56" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">容量受堆限制</text>
<text x="56" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各实例各一份</text>
<text x="170" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">多一次往返</text>
<text x="170" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全实例共享</text>
<text x="170" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">结构+持久化</text>
<text x="284" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最慢</text>
<text x="284" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据以它为准</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">命令执行为什么不做多线程：</text>
<rect x="8" y="168" width="324" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="187" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">瓶颈不是 CPU；共享状态要加锁</text>
<text x="170" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">想用多核就分片（多实例或 Cluster）</text>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单个热点 key 只在一个分片上，分片救不了</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要靠本地缓存、读从库或拆副本</text>
</svg>
读请求逐层往后找：先本地缓存，没有再问 Redis，最后才是数据库；下面是命令执行不做多线程的理由。
**业务场景。** 直播间的礼物配置几百种、读极多、一天改几次，放本地缓存每分钟刷新；打赏榜要全局共享按分数排序，放 Redis ZSet（`ZINCRBY` 加 `ZREVRANGE`），放 Memcached 就得整表取出来应用层排序；用户资产以数据库为准。某主播爆火时，他的榜单 key 只在一个分片的一个线程上，Cluster 分不开，要靠本地缓存挡一层、读从库或拆成多个副本 key。
**容易错。**
- **以为多开线程就能扩容 Redis：** 扩容靠分片。Dragonfly、KeyDB 是多线程兼容实现，先确认单实例真被 CPU 卡住再考虑。
- **以为 Cluster 能解决热点 key：** 一个 key 只在一个分片上。
