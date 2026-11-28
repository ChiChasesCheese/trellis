---
id: bagu-hot-key-1-find
node: a.cache.hot-key
type: qa
step: 1
---
## Q
**热 key · 是什么、怎么发现**｜必会

面试官：「某个主播开播，他的直播间信息 key 访问量远超其他 key，Redis 这个分片被打满。加节点有用吗？怎么发现这种 key？」

## A
**基本回答。** 热 key（hot key）是访问量远远超过其他 key 的 key。Redis Cluster 把 key 空间切成 16384 个槽（key 算 CRC16 再对 16384 取模），每个槽只属于一个主节点，一个 key 永远只在一个槽里，也就只在一个分片的主节点上，这个分片的一个 CPU 核大约能处理 8 到 10 万 QPS（每秒请求数），所以加节点没用。发现它的办法有三条：客户端或 SDK 里做滑动窗口计数（最直接、最实时）、代理层统计流量、`redis-cli --hotkeys`（要求淘汰策略是 LFU）；实时发现的热 key 经配置中心推送到所有实例。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<rect x="8" y="12" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="30.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">所有客户端：50 万 QPS 读 room:1001</text>
<line x1="58" y1="40" x2="58" y2="98" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,98.0 54.8,91.0 61.2,91.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="40" x2="170" y2="98" stroke-width="4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,98.0 166.8,91.0 173.2,91.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="282" y1="40" x2="282" y2="98" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282.0,98.0 278.8,91.0 285.2,91.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="100" width="100" height="54" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 A</text>
<text x="58.0" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽 0–5460</text>
<rect x="120" y="100" width="100" height="54" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 B</text>
<text x="170.0" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽 5461–10922</text>
<rect x="232" y="100" width="100" height="54" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 C</text>
<text x="282.0" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10923–16383</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">room:1001 的槽是 10033，只在 B</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加分片只是把别的槽搬走，这个 key 的流量</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">仍然全部打在原来那一个主节点上</text>
</svg>
所有请求都读 `room:1001`，它的槽 10033 在分片 B；粗箭头全压在 B 上，A 和 C 闲着，再加新分片也只是别的槽分出去。
**容易错。**
- **以为加节点能扩容热 key：** Cluster 里的 key 只在一个槽里，加节点解决不了单个 key 的热点。
- **以为 hotkeys 随时能用：** 淘汰策略不是 LFU 时不可用，而且它是对 keyspace 的扫描快照，不是实时发现。
- **长时间开 MONITOR：** 开销大，会拖慢本来就吃紧的节点，只能短时间在从库上用。
- **等到被打满才发现：** 能提前登记的营销热点，要在活动前就配好本地缓存和副本。
**举个例子。** 头部主播开播，`room:1001` 每秒被读 50 万次，所在分片 B 一个核只能处理 8 到 10 万次，B 上其他直播间的 key 也一起超时，A 和 C 却很空闲。运维加分片 D 只是搬走一部分槽，`room:1001` 的槽 10033 仍只有一个主节点。客户端 SDK 每秒统计各 key 访问次数，发现它超阈值，通过配置中心推给所有实例开本地缓存，流量才被分担。
