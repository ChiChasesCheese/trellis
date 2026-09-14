---
id: foundations-scale-up-vs-out
node: foundations.tradeoffs
type: qa
---
## Q
When do you keep scaling *up* (bigger machine) instead of *out* (more machines), and what eventually forces the switch?

## A
Scale up while you can: no partitioning, no rebalancing, no distributed failure modes — and a single 2026 box goes further than people assume (TBs of RAM, millions of IOPS). Costs: price grows superlinearly with size, and there's a hard ceiling.

Forced out by: load beyond the biggest box, **availability** (one machine is one failure domain), or geographic latency requiring presence in multiple regions.

DDIA's point: distribution adds irreducible complexity — go distributed when a number forces you, never by default.


## Q zh
什么时候应该继续 scale up（换更大的机器）而不是 scale out（加更多机器），最终是什么迫使你切换？

## A zh
能 scale up 就先 scale up：没有分区、没有重平衡、没有分布式故障模式 — 而且一台 2026 年的机器远比人们以为的更能扛（TB 级内存、百万级 IOPS）。代价：价格随规格超线性增长，而且存在硬性上限。

被迫转向 scale out 的原因：负载超过了最大的那台机器、**可用性**（单机就是单一故障域），或者地理延迟要求在多个地域都有部署。

DDIA 的观点：分布式带来不可消除的复杂性 — 只有当某个数字真正逼你走这条路时才走分布式，绝不默认这么做。
