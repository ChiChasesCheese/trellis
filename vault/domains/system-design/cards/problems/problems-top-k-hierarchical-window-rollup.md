---
id: problems-top-k-hierarchical-window-rollup
node: problems.search.top-k
type: qa
step: 5
tags: [grown]
---
## Q
In a Top-K design that must serve four window granularities at once (1 minute, 1 hour, 1 day, all-time), how are the coarser windows computed without reprocessing the raw event stream for each one, and which of Count-Min Sketch or Space-Saving supports this directly?

## A
Only the finest granularity (1-minute tumbling buckets) consumes the raw event stream. Coarser windows are built by rolling up buckets: an hour = 60 one-minute Count-Min Sketches summed cell-by-cell, a day = 24 hourly sketches summed, all-time = a running cell-wise sum across days — this works because CMS's update rule is linear (summing sketches is equivalent to summing the underlying streams). Space-Saving summaries do NOT support this rollup directly — a coarser window's candidate set is instead built as the union of the finer windows' candidate sets (a safe superset, since Theorem 3's guarantee only grows more items into candidacy as N grows, never fewer) and then re-ranked by querying the rolled-up CMS.

## Q zh
在一个必须同时提供 4 档时间粒度（1 分钟、1 小时、1 天、全量）的热门榜设计中，粗粒度窗口如何在不对每一档都重新消费原始事件流的情况下算出来？Count-Min Sketch 和 Space-Saving 哪一个直接支持这种做法？

## A zh
只有最细粒度（1 分钟 tumbling bucket）直接消费原始事件流。粗粒度窗口靠桶的滚动汇总得到：1 小时 = 60 个 1 分钟 Count-Min Sketch 按 cell 相加，1 天 = 24 个小时 sketch 相加，全量 = 跨天持续按 cell 累加——这成立是因为 CMS 的更新规则是线性的（sketch 相加等价于底层数据流合并后再统计）。Space-Saving 摘要不直接支持这种滚动：粗粒度窗口的候选集合改为取各细粒度窗口候选集合的并集（这是一个安全的超集，因为定理 3 的保证只会随 N 增大而让更多 item 够格成为候选，不会更少），再用滚动汇总后的 CMS 对候选重新排序。
