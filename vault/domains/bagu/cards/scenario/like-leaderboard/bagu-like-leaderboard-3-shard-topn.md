---
id: bagu-like-leaderboard-3-shard-topn
node: a.scenario.like-leaderboard
type: qa
step: 3
---
## Q
**榜单太大或单 key 热点 · 怎么分片与合并 Top N**｜必会

面试官：「榜单数据量很大，或者一个 ZSet 被打成热点，怎么办？集群下怎么分？」

## A
**基本回答。** 先控制大小：没人看几万名之后的数据，`ZREMRANGEBYRANK key 0 -1001` 删掉从最低名次到倒数第 1001 名，只留分数最高的 1000 个。全站大榜每秒更新都落同一个 key，所在节点 CPU 打满，所以按 ID 哈希分到 S 个 ZSet，key 显式命名如 `rank:{0..S-1}`（Cluster 里一个 key 只在一个节点），每片各自维护 Top N；查询时每片取 Top N，在应用层归并（`heapq.nlargest`）。归并放应用层，因为跨片 `ZUNIONSTORE` 要求同槽，而分片本来就为了落在不同节点。结果准确：全局 Top N 的元素必在自己分片的 Top N 里，否则该片至少有 N 个比它大的，它在全局至少排 N+1。按房间、类目拆榜本身就是天然分散。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按 ID 哈希分到 S 个 ZSet，各自维护 Top N</text>
<rect x="8" y="24" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 0</text>
<text x="58" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">局部 Top N</text>
<line x1="58" y1="64" x2="58.0" y2="85.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58,92 54.8,85.0 61.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="24" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 1</text>
<text x="170" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">局部 Top N</text>
<line x1="170" y1="64" x2="170.0" y2="85.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,92 166.8,85.0 173.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="24" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 2</text>
<text x="282" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">局部 Top N</text>
<line x1="282" y1="64" x2="282.0" y2="85.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282,92 278.8,85.0 285.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="92" width="324" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用层归并：取分数最大的 N 个</text>
<line x1="170" y1="128" x2="170.0" y2="141.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,148 166.8,141.0 173.2,141.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="148" width="324" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全局 Top N</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">全局前 N 必在各自分片的前 N 里</text>
</svg>
每个分片只管局部 Top N，读取时在应用层合并各片结果，取分数最大的 N 个。
**举个例子。** 3 个分片取全局 Top 2，每片取前 2：分片 0 是 a=90、b=50，分片 1 是 c=80、d=70，分片 2 是 e=60、f=55；归并取最大 2 个得 a=90、c=80。
```python
import heapq
# 每片先 ZREVRANGE 取各自的 Top N，得到 (成员, 分数) 列表
def global_top(shards, n):
    return heapq.nlargest(n, (x for s in shards for x in s), key=lambda x: x[1])
```
**业务场景。** 全站点赞榜每秒 5 万次 `ZINCRBY` 打同一个 key、节点 CPU 打满；拆成 16 片后每片约 3000 次每秒，归并只发生在读取时。
**容易错。**
- **每片只取一个：** 全局第 2 名可能和第 1 名同片，每片要取 N 个。
