---
id: foundations-latency-numbers-in-arguments
node: foundations.numbers
type: qa
---
## Q
A p99 budget is 200 ms and each service hop costs ~0.5 ms of same-DC RTT plus its own work. What design smell do the latency numbers expose in a 10-microservice synchronous call chain?

## A
Network RTT itself is cheap (~5 ms for 10 hops) — the real costs are **per-hop p99 amplification** (the slowest of many hops dominates; tail latencies compound) and any hop that touches disk (~10 ms) or crosses a region (~100 ms).

Rule: budget in orders of magnitude — one cross-region call can outweigh dozens of in-DC hops.


## Q zh
p99 预算是 200 ms，每个服务跳转花费约 0.5 ms 的同 DC RTT 加上自身的处理时间。在一个 10 微服务的同步调用链中，这些延迟数字暴露了什么设计问题？

## A zh
网络 RTT 本身很便宜（10 跳约 5 ms）— 真正的成本是**每跳的 p99 放大**（众多跳中最慢的那个主导整体；尾部延迟会叠加）以及任何触碰磁盘（约 10 ms）或跨地域（约 100 ms）的跳转。

规则：按数量级来做预算 — 一次跨地域调用的代价可以超过几十个同 DC 内的跳转。
