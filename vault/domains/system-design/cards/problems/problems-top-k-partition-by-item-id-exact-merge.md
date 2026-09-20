---
id: problems-top-k-partition-by-item-id-exact-merge
node: problems.search.top-k
type: qa
step: 2
tags: [grown]
---
## Q
In a Top-K trending design with no dimension slicing (just a single global ranking), why does partitioning the ingestion stream by item_id — rather than round-robin across consumers — let per-shard local Top-K lists be merged into a globally exact result with a simple K-way merge, and what breaks if you partition round-robin instead?

## A
Partitioning by `item_id` (hashing the key) guarantees every event for a given item lands on the same shard, so each shard's item set is disjoint from every other shard's — a shard's locally-computed exact count for an item IS the item's true global count, and its local Top-K list is final for those items. Merging then reduces to a lossless K-way merge of S sorted lists (O(S*K*log S), no sketches needed). Round-robin (or any key-independent) partitioning splits one item's events across many shards; each shard sees only a fraction of that item's count, so it may never rank high enough to enter any single shard's local Top-K list, and a naive K-way merge of the local lists silently drops it even though its true global count is large.

## Q zh
在一个没有维度切片（只有单一全局排行）的热门榜设计中，为什么按 item_id 对摄入流分区（而不是轮询分给多个 consumer）能让各分片的局部 Top-K 列表通过一次简单的 K 路归并就得到全局精确结果？如果改成轮询分区会出什么问题？

## A zh
按 `item_id` 哈希分区能保证同一个 item 的所有事件都落在同一个分片上，所以每个分片的 item 集合和其他分片互不相交——一个分片本地算出的某 item 精确计数就是该 item 的全局真实计数，其局部 Top-K 列表对这些 item 而言就是最终结果。合并因此退化为对 S 个有序列表的无损 K 路归并（`O(S*K*log S)`），不需要任何 sketch。而轮询（或任何与 key 无关）的分区会把同一个 item 的事件分散到多个分片，每个分片只看到它计数的一小部分，可能在任何一个分片的局部 Top-K 里都排不进去，对局部列表做朴素 K 路归并会悄悄漏掉这个真实全局计数很高的 item。
