---
id: problems-social-graph-search-typed-edge-inverted-index
node: problems.social.social-graph-search
type: qa
step: 3
tags: [grown]
---
## Q
In a social graph store that holds multiple edge types (friend, follow, blocked) in the same underlying storage, why does indexing by the composite key `(edgeType, srcId)` — each mapping to a posting list of target ids — outperform a single `(srcId)` index that filters by edge type at the application layer?

## A
A single `(srcId)` index returns every edge for that user regardless of type, forcing the application to read rows it doesn't need and discard them after the fact whenever edge types are unevenly distributed. Indexing by `(edgeType, srcId)` lets the index itself narrow the scan to exactly the requested type's posting list before any rows are read — structurally the same idea as an inverted index mapping a search term to a list of matching document ids, just with 'edge type + source user' playing the role of the term.

## Q zh
在一个把多种边类型（好友、关注、拉黑）存在同一份底层存储里的社交图存储中，为什么按复合键 `(edgeType, srcId)`——每个键映射到一份目标 id 的倒排列表（posting list）——建索引，会比只用单一 `(srcId)` 索引、在应用层按边类型过滤更好？

## A zh
单一的 `(srcId)` 索引会返回该用户的全部边而不管类型，一旦边类型分布不均，应用层就得读一堆用不到的行再事后丢弃。按 `(edgeType, srcId)` 建索引，能让索引本身在读任何行之前就把扫描范围收窄到请求的那个类型对应的倒排列表——结构上和「搜索词映射到匹配文档 id 列表」的倒排索引是同一个思路，只是这里「边类型 + 源用户」扮演了词项的角色。
