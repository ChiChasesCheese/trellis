---
id: problems-typeahead-10x-hot-cold-split-fst
node: problems.search.typeahead
type: qa
step: 8
tags: [grown]
---
## Q
In a typeahead design scaling from 300M to 3B DAU (10x), the precomputed prefix structure grows from about 12GB to about 120GB, which is still affordable in memory. What optimization becomes worthwhile at this scale, and how does it split the cache?

## A
Once a large fraction of prefixes have stopped changing meaningfully (their candidate rankings are stable), it becomes worthwhile to split the prefix cache into a 'hot' region — prefixes still receiving frequent incremental patches, kept as the mutable trie-with-cache structure — and a 'cold' region — stable prefixes rebuilt periodically as a read-only FST snapshot, trading FST's inability to update incrementally for its superior memory compression, since stable prefixes don't need frequent patching anyway. Prefixes are routed to whichever region currently holds them based on how recently their ranking has changed.

## Q zh
在一个从 3 亿日活扩展到 30 亿日活（10 倍）的 typeahead 设计中，预计算的前缀结构从约 12GB 增长到约 120GB，仍然可以放进内存。在这个规模下，什么优化变得值得做？它如何拆分缓存？

## A zh
一旦相当一部分前缀的候选排名已经趋于稳定、不再频繁变化，把前缀缓存拆成'热区'和'冷区'两部分就变得值得：热区是仍在频繁接收增量补丁的前缀，继续用可变的 trie + 缓存结构；冷区是排名已经稳定的前缀，周期性整体重建为只读的 FST 快照，用 FST 无法增量更新的代价换取它更高的内存压缩率——反正稳定前缀本来也不需要频繁打补丁。请求按某个前缀最近一次排名变化的时间，路由到当前持有它的那个区域。
