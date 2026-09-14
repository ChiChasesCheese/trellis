---
id: fnd-perf-throughput-tail
node: foundations.performance
type: qa
---
## Q
During a benchmark, throughput rises with offered load until p99 suddenly collapses. Where is the useful operating point?

## A
Not at maximum throughput. Operate before the **latency knee**, where utilization leaves enough headroom for bursts, skew, failures, and background work. Find it by plotting offered load, achieved throughput, errors, queue time, and tail latency together; capacity is the highest load that still meets the SLO, not the largest QPS printed by the tool.

## Q zh
benchmark 中，throughput 随 offered load 上升，直到 p99 突然崩溃。真正有用的 operating point 在哪里？

## A zh
不在 maximum throughput。应运行在 **latency knee** 之前，给 burst、skew、failure 和 background work 留出 headroom。把 offered load、achieved throughput、error、queue time、tail latency 画在一起；capacity 是仍满足 SLO 的最高负载，而不是工具打印出的最大 QPS。
