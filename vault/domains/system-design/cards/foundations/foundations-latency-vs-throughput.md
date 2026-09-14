---
id: foundations-latency-vs-throughput
node: foundations.tradeoffs
type: qa
---
## Q
Batching writes raises throughput but hurts which metric, and why? Name the general trade-off.

## A
**Latency vs throughput.** Batching amortizes fixed per-request costs (syscalls, network frames, fsyncs) across many items — throughput up — but each item now waits for its batch to fill or a flush timer, so per-item latency rises.

The lever appears everywhere: Kafka `linger.ms`, group commit in databases, Nagle's algorithm. Choose by whether the path is user-facing (latency wins) or bulk/async (throughput wins).


## Q zh
批处理写提高吞吐量但伤害哪个指标，为什么？说出总的权衡。

## A zh
**延迟 vs 吞吐量。** 批处理在许多项目中摊销每请求的固定成本（syscalls、网络帧、fsyncs） — 吞吐量上升 — 但每一项现在要等待它的批处理填满或刷新计时器，所以每项延迟上升。

这个杠杆无处不在：Kafka `linger.ms`、数据库中的组提交、Nagle 算法。选择取决于路径是面向用户（延迟胜）还是批量/异步（吞吐量胜）。
