---
id: fnd-perf-coordinated-omission
node: foundations.performance
type: qa
---
## Q
A load generator waits for each response before sending the next request. Why can it report a healthy p99 during a server pause?

## A
It suffers **coordinated omission**: while the server is paused, the generator also stops creating the requests that real independent users would have sent, so their queueing delay is absent from the sample. Use an open-loop or fixed-arrival-rate workload, record intended start times, and report timeout/failure rates with latency.

## Q zh
一个 load generator 等每个响应回来后才发下一个请求。为什么服务暂停时，它仍可能报告健康的 p99？

## A zh
这是 **coordinated omission**：服务暂停时 generator 也停止生成真实独立用户本来会发出的请求，因此样本里缺少这些请求的 queueing delay。使用 open-loop 或 fixed-arrival-rate workload，记录 intended start time，并把 timeout/failure rate 与 latency 一起报告。
