---
id: problems-ad-click-aggregation-late-data-three-tiers
node: problems.search.ad-click-aggregation
type: qa
step: 5
tags: [grown]
---
## Q
In an ad click aggregation design, describe the three-tier policy for handling a click event that arrives after its window's watermark has passed, from least to most costly to handle.

## A
(1) Within the allowed-lateness grace period after the window closes: the window re-triggers, recomputing and emitting a retraction plus a corrected value (see the watermark/retraction card). (2) After the grace period but before the daily reconciliation cutoff: the streaming layer no longer re-triggers that window (to avoid windows staying open indefinitely); the event is instead side-outputted to a separate late-events stream and only folded in by the next batch reconciliation run. (3) After the reconciliation cutoff (e.g. 48 hours after the event's own timestamp): the event is treated as anomalous and routed to a manual/fraud-review path rather than being auto-applied to the billing ledger, since a click arriving that late is itself suspicious.

## Q zh
在一个广告点击聚合设计中，描述对「到达时其所在窗口的水位线已经过去」的点击事件的三层处理策略，按处理代价从低到高排列。

## A zh
(1) 在窗口关闭后的允许迟到宽限期内：窗口重新触发，重新计算并发出一次撤回加一个修正后的值（见水位线/撤回卡片）。(2) 超过宽限期、但在每日对账截止时间之前：流式层不再对该窗口重新触发（避免窗口无限期悬而不决），该事件改为侧输出到一个单独的「迟到事件」流，只在下一次批处理对账时才被并入。(3) 超过对账截止时间（例如事件自身时间戳之后 48 小时）：视为异常，转入人工/反欺诈复核流程，而不是自动应用到计费账本上——一次点击迟到这么久本身就值得怀疑。
