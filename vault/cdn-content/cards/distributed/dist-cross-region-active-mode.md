---
id: dist-cross-region-active-mode
node: distributed.cross-region
type: qa
---
## Q
Choose active-active or active-passive for a global content service. What is the decisive trade-off?

## A
Active-active gives low local latency and uses all capacity, but requires conflict-free ownership, global routing, replication-lag handling, and enough spare capacity for regional loss. Active-passive simplifies write consistency and incident control, but pays failover RTO, cold capacity/cache risk, and potentially higher normal latency. Choose from state ownership and recovery objectives, not from the desire to call the architecture “global.”

## Q zh
全球 content service 应选 active-active 还是 active-passive？决定性 trade-off 是什么？

## A zh
active-active 提供低本地 latency 并使用全部容量，但要求 conflict-free ownership、global routing、处理 replication lag，并为 region loss 保留足够 spare capacity。active-passive 简化 write consistency 与 incident control，却要支付 failover RTO、cold capacity/cache 风险及可能更高的正常 latency。应由 state ownership 与 recovery objective 决定，而不是为了把架构称为 “global”。
