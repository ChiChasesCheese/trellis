---
id: reliability-three-region-quorum
node: reliability.multi-region
type: qa
---
## Q
Why does surviving a full region loss with zero data loss require three regions, not two — and what is the cheap third-region trick?

## A
Synchronous consensus/quorum replication needs a **majority**. With 2 regions, any split or region loss leaves at most half the replicas — no majority, so you either stall (unavailable) or fail over asynchronously (lose data). With replicas spread across **3 regions**, losing any one still leaves 2/3 — writes continue, RPO stays 0.

Cost trick: make the third region a **witness/tiebreaker** — it stores only quorum votes/log metadata, not full data or serving capacity.

Price: every commit waits for the **nearest other region's RTT**, so region choice (two close + one far) sets your write latency floor.

## Q zh
为什么生存完整区域丢失零数据丢失需要三个区域，不是两个——便宜的第三区域技巧是什么？

## A zh
同步共识/quorum 复制需要**多数**。有 2 个区域，任何分裂或区域丢失最多剩下一半副本——无多数，所以你要么停止（不可用）要么异步故障转移（丢失数据）。有副本跨**3 个区域**，丢失任何一个仍然剩下 2/3——写继续，RPO 保持 0。

成本技巧：使第三区域**见证/打破平手** ——它只存储 quorum 投票/日志元数据，不是完整数据或服务容量。

价格：每个提交等待**最近其他区域的 RTT**，所以区域选择（两个近 + 一个远）设置你的写延迟下限。
