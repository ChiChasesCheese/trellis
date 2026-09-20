---
id: problems-ad-click-aggregation-watermark-heuristic-retraction
node: problems.search.ad-click-aggregation
type: qa
step: 4
tags: [grown]
---
## Q
According to Google's Dataflow model, is a watermark a correctness guarantee that all data up to a given event time has arrived? In an ad click aggregation design, what mechanism does this force when a window re-triggers after new late data arrives?

## A
No — the Dataflow paper is explicit that a watermark is only a heuristic estimate of when the system thinks data up to that point has likely all arrived, not a guarantee ('we won't rely on watermarks as such'). Because of this, a window can legitimately re-trigger after emitting a result, if a late event arrives within the allowed-lateness grace period. Simply overwriting the old emitted value with the new one is unsafe if any downstream stage does a second grouping/aggregation on top of the first result — that downstream stage would then double-count the old and new values as separate inputs. The fix is Accumulating & Retracting: emit an explicit retraction of the previous value before emitting the corrected one, so downstream aggregations can subtract the old contribution before adding the new one.

## Q zh
根据 Google 的 Dataflow 模型，水位线（watermark）是不是「某个事件时间之前的数据都已到齐」的正确性保证？在广告点击聚合设计中，当一个窗口因为新到达的迟到数据而重新触发时，这逼出了什么机制？

## A zh
不是——Dataflow 论文明确说水位线只是系统对「这个时间点之前的数据大概率都到齐了」的一个启发式估计，不是保证（原文："we won't rely on watermarks as such"）。正因如此，一个窗口在发出结果之后，如果迟到事件落在允许的宽限期内，是可以合法地重新触发的。如果下游还有基于这个聚合结果做的二级分组/聚合，直接用新值覆盖旧值是不安全的——下游会把新旧两个值当成两笔独立输入重复计入。解决办法是 Accumulating & Retracting（累积与撤回）：重新触发前先显式发出对上一次值的撤回，再发出修正后的新值，这样下游聚合才能先减去旧贡献再加上新贡献。
