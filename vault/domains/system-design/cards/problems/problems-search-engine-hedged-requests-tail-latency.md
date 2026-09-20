---
id: problems-search-engine-hedged-requests-tail-latency
node: problems.search.search-engine
type: qa
step: 4
tags: [grown]
---
## Q
In a document-partitioned search index with 480 shards where each shard independently has a 1% chance of missing its latency budget, the probability that a query touching all 480 shards hits at least one slow shard is about 99.2% (1 - 0.99^480). How does issuing a hedged (duplicate) request to a slow shard after a short wait reduce this, and by how much under the assumption that the original and hedge failures are independent?

## A
A hedged request sends a second, redundant request to an independent replica of any shard that hasn't responded after a short wait (e.g. around the historical P50 latency); the query uses whichever of the two responses returns first. If a single request has a 1% chance of being slow and the hedge's slowness is independent of the original's, the probability that BOTH are slow is 0.01 x 0.01 = 0.0001 (0.01%). Recomputing the fan-out formula with this effective per-shard miss probability, 1 - 0.9999^480 ≈ 4.7% — roughly a 20x reduction in the probability that the overall query misses its latency budget, at the cost of the extra load from the (relatively rare) hedge requests.

## Q zh
在一个按文档分片、共 480 个分片的搜索索引中，假设每个分片独立地有 1% 的概率超出延迟预算，一次触达全部 480 个分片的查询命中至少一个慢分片的概率约为 99.2%（1 - 0.99^480）。在原始请求和对冲请求的'慢'相互独立这一假设下，向等待一小段时间仍未返回的慢分片发送一次对冲（重复）请求，能把这个概率降低多少？

## A zh
对冲请求是指：对任何在短暂等待（比如历史 P50 延迟附近）后仍未返回的分片，向它的一个独立副本再发一次请求，两次请求谁先返回就用谁的结果。如果单次请求有 1% 的概率变慢，且对冲请求的变慢与原始请求相互独立，那么'两次都慢'的概率是 0.01×0.01=0.0001（0.01%）。把这个有效的单分片超预算概率重新代入扇出公式，1-0.9999^480≈4.7%——整体查询命中长尾的概率降低约 20 倍，代价是对冲请求（本身占比不高）带来的额外负载。
