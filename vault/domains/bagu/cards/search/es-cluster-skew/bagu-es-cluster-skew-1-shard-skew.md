---
id: bagu-es-cluster-skew-1-shard-skew
node: b.search.es-cluster-skew
type: qa
step: 1
---
## Q
**ES 集群 · 分片规划与数据倾斜**｜追问

面试官：「ES 的数据倾斜是什么，怎么发现、怎么解决？分片数怎么规划？」

## A
**基本回答。** 数据倾斜是数据或读写集中在少数分片上，这些分片所在节点的 heap、GC、延迟先出问题。路由决定文档去哪个分片：对路由值取哈希再对主分片数取模，路由值不均匀分片就不均匀；成因有按商家 ID 路由（大商家写量极高）、时序数据只写最新索引、热词搜索让查询集中。发现：`GET _cat/shards?v&s=store` 找偏大的分片，`_nodes/stats` 看节点 heap 和 CPU，`_stats/indexing`、`_stats/search` 看读写热点。解决：自定义 routing 加盐（如用户 ID 加小时数取哈希），或 `index.routing_partition_size` 让同一路由值分布到一组分片，代价是搜索要查更多分片；时序数据用 rollover 加 ILM，索引到阈值就滚出新索引；再冷热分层，老数据移出热节点。分片规划：单分片 10GB 到 50GB；主分片数建索引时固定，之后只能 split 或 reindex，要留余量，也别切成大量小分片。副本救不了写入倾斜：写入先到主分片再同步副本，副本越多写入工作越多，副本只提高读吞吐和可用性。查询热点用 request cache 或 Redis，深分页改 `search_after`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个索引的 5 个主分片大小（示意）</text>
<text x="6" y="39" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 0</text>
<rect x="56" y="24" width="50" height="22" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="6" y="67" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 1</text>
<rect x="56" y="52" width="70" height="22" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="6" y="95" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 2</text>
<rect x="56" y="80" width="250" height="22" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="181" y="95" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头部商家都路由到这里</text>
<text x="6" y="123" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 3</text>
<rect x="56" y="108" width="40" height="22" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="6" y="151" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 4</text>
<rect x="56" y="136" width="60" height="22" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="6" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最大的分片所在节点：heap、GC、延迟先出问题</text>
</svg>
每行是一个分片的数据量。按商家 ID 路由时，头部商家把其中一个分片撑得远大于别的。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 168">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">别名 orders-write 始终指向最新的索引</text>
<rect x="6" y="26" width="104" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">orders-000001</text>
<line x1="110" y1="41" x2="113.0" y2="41.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120,41 113.0,44.2 113.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="26" width="104" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="172" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">orders-000002</text>
<line x1="224" y1="41" x2="227.0" y2="41.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="234,41 227.0,44.2 227.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="234" y="26" width="104" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">orders-000003</text>
<text x="6" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">冷节点</text>
<text x="120" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">温节点</text>
<text x="234" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">热节点（写入）</text>
<text x="6" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">达到大小、文档数或存在时间条件就 rollover</text>
<text x="6" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每个索引大小均匀，老索引移到温节点或冷节点</text>
<text x="6" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最新索引不再因为越长越大而成为热点</text>
</svg>
时序数据用 rollover 滚动新索引，写入始终在最新的一个，老的逐步降温。
**举个例子。** 订单索引 5 个主分片按商家 ID 路由：头部商家 A 的 `hash(A) % 5` 总是分片 2，全部写入和数据压在它上，所在节点搜索延迟飙升；`_cat/shards` 按大小排序可见分片 2 偏大。改用商家 ID 加小时数取哈希后各分片均衡，代价是按商家查询要查更多分片。
**容易错。**
- **以为加副本能解决写入倾斜：** 见上，热点主分片的写入压力不降。
- **只看节点 CPU 不看分片大小：** `_cat/shards` 才能最先发现倾斜。
