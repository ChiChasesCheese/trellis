---
id: delivery-shadow-capacity
node: delivery.shadow
type: qa
---
## Q
Why can a 100% dark launch cause an outage even though users never receive shadow responses?

## A
Mirroring can double origin calls, network bytes, CPU, connection pools, logs, and downstream rate-limit consumption. Start with a bounded sample, model amplification by request class, isolate queues and concurrency, and shed shadow work first. Shadow fidelity is useful only while production goodput and SLOs remain protected.

## Q zh
为什么 100% dark launch 可能导致 outage，即使用户永远不会收到 shadow response？

## A zh
mirroring 可能让 origin call、network byte、CPU、connection pool、log 和 downstream rate-limit consumption 翻倍。应从 bounded sample 开始，按 request class 建模 amplification，隔离 queue 与 concurrency，并优先 shed shadow work。只有在 production goodput 和 SLO 受到保护时，shadow fidelity 才有价值。
