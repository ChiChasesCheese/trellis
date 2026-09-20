---
id: problems-top-k-cms-vs-space-saving-tradeoff
node: problems.search.top-k
type: qa
step: 3
tags: [grown]
---
## Q
In a Top-K trending design, why do systems typically run a Count-Min Sketch (CMS) and a Space-Saving structure side by side instead of picking just one of the two?

## A
The two structures cover complementary gaps. CMS answers point queries for a known key with a mergeable, linear update rule — summing two independently-maintained CMS's cell-by-cell gives exactly the same result as running one CMS over the combined stream — but it cannot enumerate which keys are frequent; you must already know which item_id to ask about. Space-Saving does enumerate: it maintains a bounded candidate set with a deterministic guarantee that any sufficiently frequent item is in it, but merging two Space-Saving summaries by adding their counters does not reproduce the guarantee you'd get from running Space-Saving on the combined stream, so it doesn't merge cleanly across shards. The combination used is: Space-Saving (per shard) to discover which item_ids are worth asking about, CMS (merged across shards by summing cells) to get a merge-safe, error-bounded count for each candidate.

## Q zh
在一个热门榜设计中，为什么系统通常会同时运行 Count-Min Sketch（CMS）和 Space-Saving 两种结构，而不是只选其中一个？

## A zh
这两种结构互补了彼此的缺口。CMS 用线性的更新规则回答「某个已知 key 的计数是多少」这类点查询，且天然可合并——把两个独立维护的 CMS 逐 cell 相加，结果和把两路数据流合并后跑一个 CMS 完全一样——但它无法枚举出哪些 key 是热门的，你必须已经知道要问哪个 item_id。Space-Saving 恰好能枚举：它维护一个有界的候选集合，并保证任何频次足够高的 item 一定在其中，但把两份 Space-Saving 摘要的计数器直接相加，并不能复现「对合并后的流跑一遍 Space-Saving」应有的保证，所以它在跨分片场景下不能干净地合并。实际用法是：每个分片用 Space-Saving 发现「哪些 item_id 值得问」，再用跨分片按 cell 相加合并后的 CMS 给出每个候选的、误差有界且合并安全的计数。
