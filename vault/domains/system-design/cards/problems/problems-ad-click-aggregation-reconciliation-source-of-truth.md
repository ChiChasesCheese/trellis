---
id: problems-ad-click-aggregation-reconciliation-source-of-truth
node: problems.search.ad-click-aggregation
type: qa
step: 8
tags: [grown]
---
## Q
In an ad click aggregation design, why is the streaming aggregation result never treated as the final billing figure, and what does the daily reconciliation job actually establish?

## A
The streaming result's completeness rests on the watermark, which is only ever a heuristic estimate of when data has likely all arrived (per the Dataflow model), never a proof — so no amount of tuning the watermark or the allowed-lateness window can make the streaming result provably final. The design instead runs a nightly batch job over the immutable raw click log for the previous day, recomputing counts with no watermark constraint at all (it simply waits until the whole day's log is available), and compares that recount against the streaming result per `(ad_id, day)`. Only rows where the two agree exactly are marked `is_reconciled=true` and treated as the final billing figure; any discrepancy is corrected with an auditable, logged change rather than a silent overwrite. This is the same lambda-architecture pattern (fast approximate layer plus a slower authoritative batch layer) applied specifically to make billing correctness provable rather than merely probable.

## Q zh
在一个广告点击聚合设计中，为什么流式聚合的结果从不被当作最终计费数字？每日对账任务实际确立的是什么？

## A zh
流式结果的完整性依赖水位线，而水位线（按 Dataflow 模型）永远只是「数据大概率已到齐」的启发式估计，从来不是证明——无论怎么调水位线或允许迟到的宽限期，都不能让流式结果被证明为最终值。设计上改为每天对前一天不可变的原始点击日志跑一次批处理任务，完全不受水位线约束地重新计数（只是简单地等整天的日志都齐了），再按 `(ad_id, day)` 和流式结果比较。只有两者完全一致的行才被标记 `is_reconciled=true`、当作最终计费数字；任何分歧都通过一条可审计、留痕的更正记录来修正，而不是静默覆盖。这就是 lambda 架构模式（快速的近似层加一个较慢的权威批处理层）专门用来让计费正确性「可证明」而不只是「大概率正确」的具体应用。
