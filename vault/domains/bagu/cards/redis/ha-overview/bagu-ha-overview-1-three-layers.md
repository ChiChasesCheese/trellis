---
id: bagu-ha-overview-1-three-layers
node: a.redis.ha-overview
type: qa
step: 1
---
## Q
**高可用总览 · 主从、哨兵、Cluster 各解决什么**｜必会

面试官：「大促前要把单机 Redis 升级成高可用方案。主从、哨兵、Cluster 分别解决什么问题，怎么选？」

## A
**基本回答。** 三层叠加。主从复制：主库异步复制给从库，解决数据冗余和读扩展，主库挂了要人手动切。哨兵（Sentinel）：独立监控进程，发现故障、自动选新主、通知客户端，数据仍是一份、不分片，容量和写入上限还是单机；至少 3 个，分在不同机器。Cluster：按哈希槽分片到多个主节点，每个带从节点，内置故障转移（不再需要哨兵），同时解决容量、写吞吐和高可用；局限是多键命令要求同槽、只支持 0 号库、客户端要支持重定向。选择：数据量和写入在单机以内、只要高可用用哨兵；逼近单机上限用 Cluster。共同软肋：三者都建立在异步复制上，切换时可能丢最近几条写，要主动说出。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="8" y="8" width="100" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主从复制</text>
<rect x="116" y="8" width="216" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="224" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据有多份：冗余 + 读扩展</text>
<text x="224" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库挂了要人来切</text>
<line x1="58" y1="58" x2="58" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,80 54.8,73.0 61.2,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="80" width="100" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">哨兵 Sentinel</text>
<rect x="116" y="80" width="216" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="224" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">自动发现故障、选新主、通知</text>
<text x="224" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仍是一份数据，不分片</text>
<line x1="58" y1="130" x2="58" y2="152" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,152 54.8,145.0 61.2,145.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="152" width="100" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Cluster</text>
<rect x="116" y="152" width="216" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="224" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按哈希槽分片，每片带从库</text>
<text x="224" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内置切换：容量、写入、可用</text>
<text x="66" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">+ 自动切换</text>
<text x="66" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">+ 分片</text>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三者都是异步复制：切换可能丢最后几条写</text>
</svg>
每往下一层多解决一个问题；最下一行是三者共同的软肋。
**业务场景。** 打赏榜和扣币缓存：单机挂了全停；加主从后主库宕机要运维手动提升从库、改应用配置，恢复取决于有没有人值守；加 3 个哨兵后自动选新主，恢复缩短到几十秒；写入涨到每秒 8 万、内存 40GB 后单机装不下也写不动，换 Cluster。不管哪一层，最后几条未复制的写都可能丢，所以扣币以数据库为准，Redis 只做加速。
**容易错。**
- **以为主从就是高可用。**
- **以为哨兵能解决容量问题。**
- **以为三层都不丢数据。**
