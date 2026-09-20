---
id: problems-top-k-dimension-sharding-merge-correctness
node: problems.search.top-k
type: qa
step: 6
tags: [grown]
---
## Q
In a Top-K design where a single dimension (e.g. one country) is further sub-sharded across multiple workers because its traffic is too large for one node — so the sub-shards see overlapping item sets — why is unioning or truncating each sub-shard's local Top-K list the wrong way to compute that dimension's global Top-K, and what is the correct two-step merge?

## A
An item can be popular in aggregate while being only moderately popular on every individual sub-shard — e.g. spread evenly across 8 sub-shards, never ranking high enough locally to make any single sub-shard's Top-K list — so naively unioning or truncating the sub-shards' local Top-K lists silently drops items whose true combined frequency is large. The correct merge: (1) take the union of each sub-shard's Space-Saving candidate-id set (a safe superset per its zero-false-negative guarantee), and (2) sum the sub-shards' Count-Min Sketches cell-by-cell to get a merge-correct combined sketch, then query it for each candidate's count and rank by that.

## Q zh
在一个热门榜设计中，某个维度（例如某个国家）因为流量太大又被再切分给多个子分片处理，导致这些子分片看到的 item 集合互相重叠——为什么把各子分片的局部 Top-K 列表直接取并集或截断拼接是算出该维度全局 Top-K 的错误做法？正确的两步合并是什么？

## A zh
一个 item 完全可能整体很热，但在每一个单独的子分片上都只是中等热度——比如被平均分散在 8 个子分片上，在任何一个子分片本地都排不进它的局部 Top-K 列表——所以直接对各子分片的局部 Top-K 列表取并集或截断拼接，会悄悄漏掉那些真实合计频次很高的 item。正确的合并分两步：(1) 取各子分片 Space-Saving 候选 id 集合的并集（凭借其零漏报保证，这是一个安全的超集）；(2) 把各子分片的 Count-Min Sketch 按 cell 相加得到一个合并正确的组合 sketch，再用它查询每个候选的计数并据此排序。
