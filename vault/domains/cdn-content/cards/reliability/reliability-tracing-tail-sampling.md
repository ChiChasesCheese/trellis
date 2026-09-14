---
id: reliability-tracing-tail-sampling
node: reliability.tracing
type: qa
---
## Q
Head sampling drops most traffic before latency is known, so rare 8-second requests disappear. What sampling change preserves these traces, and what is its cost?

## A
Use tail sampling in a collector to retain errors and spans exceeding latency thresholds after the trace completes, while sampling ordinary success aggressively. It requires buffering trace state, consistent routing to the collector, bounded memory, and a failure policy. Keep some unbiased baseline sampling or the retained set will be excellent for diagnosis but distorted for population estimates.

## Q zh
head sampling 在 latency 已知前丢弃大多数 traffic，导致罕见的 8-second request 消失。什么 sampling change 能保留这些 trace，代价是什么？

## A zh
在 collector 中使用 tail sampling，在 trace 完成后保留 error 和超过 latency threshold 的 span，同时大幅 sample 普通 success。它需要 buffer trace state、把同一 trace 一致路由到 collector、限制 memory，并定义 failure policy。仍应保留一部分 unbiased baseline sampling，否则 retained set 虽适合 diagnosis，却会扭曲 population estimate。
