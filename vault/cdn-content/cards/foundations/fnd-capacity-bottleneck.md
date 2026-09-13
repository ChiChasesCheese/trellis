---
id: fnd-capacity-bottleneck
node: foundations.capacity
type: qa
---
## Q
CPU is only 35% when a cache service stops scaling. Why is fleet-average CPU insufficient, and how do you find the real bottleneck?

## A
Average CPU can hide one saturated shard, core, NIC, lock, connection pool, memory bandwidth, or downstream quota. Correlate throughput with per-shard/per-core utilization, queue time, saturation and errors; change one resource or workload dimension and see whether the knee moves. The bottleneck is the constrained resource whose relief increases SLO-compliant throughput.

## Q zh
cache service 停止扩展时 CPU 只有 35%。为什么 fleet-average CPU 不够？怎样找真正 bottleneck？

## A zh
average CPU 可能掩盖单个饱和 shard、core、NIC、lock、connection pool、memory bandwidth 或 downstream quota。把 throughput 与 per-shard/per-core utilization、queue time、saturation、error 关联起来；一次改变一个资源或 workload dimension，看 latency knee 是否移动。解除后能提高 SLO-compliant throughput 的受限资源，才是真正 bottleneck。
