---
id: dist-cross-region-failover-capacity
node: distributed.cross-region
type: qa
---
## Q
Two regions each run at 70% utilization. Can either safely absorb the other after failover?

## A
No: losing one sends roughly 140% of one region's capacity before accounting for retries, cold caches, and degraded dependencies. N+1 regional resilience requires normal load low enough that survivors can absorb redirected traffic with headroom. Test the failover workload, warm critical objects, shed optional traffic, and ramp routing. A configured failover target is not failover capacity.

## Q zh
两个 region 平时都运行在 70% utilization。一个能否在 failover 后安全吸收另一个？

## A zh
不能：损失一个 region 会把约 140% 的单 region capacity 压到幸存者上，还没算 retry、cold cache 和 degraded dependency。N+1 regional resilience 要求正常负载足够低，使 survivor 有 headroom 接收重定向流量。应测试 failover workload、warm critical object、shed optional traffic，并逐步 ramp routing。配置了 failover target，不等于拥有 failover capacity。
