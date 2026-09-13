---
id: fnd-capacity-bandwidth
node: foundations.capacity
type: qa
---
## Q
A POP serves 20k responses/s with a 500 KiB average body. What first-order network capacity does that imply, and what caveats must the plan add?

## A
Payload alone is about `20,000 × 500 KiB ≈ 10 GiB/s ≈ 80 Gib/s`. Add protocol overhead, retransmits, uneven object sizes, ingress traffic, burst and failover headroom, and NIC/link redundancy. Use p95 byte rate and traffic shape as well as averages; a few large objects can dominate bandwidth while small requests dominate QPS.

## Q zh
一个 POP 每秒服务 20k 个响应，平均 body 为 500 KiB。一阶 network capacity 是多少？规划时还要加哪些因素？

## A zh
仅 payload 就约为 `20,000 × 500 KiB ≈ 10 GiB/s ≈ 80 Gib/s`。还要加入 protocol overhead、retransmit、object size 不均、ingress traffic、burst/failover headroom，以及 NIC/link redundancy。除 average 外还要看 p95 byte rate 与 traffic shape；少量大 object 可能主导 bandwidth，而小请求主导 QPS。
