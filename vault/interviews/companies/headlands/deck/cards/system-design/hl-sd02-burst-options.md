---
id: hl-sd02-burst-options
node: system-design.sd02-job-scheduler
type: qa
step: 26
---
## Q
整点 2.08×10⁵ 个任务同时到期，有哪四种手段保证 Δ？

## A
1. **提供足够的分发能力**：分发器批量发布到队列（批 1,000 条、多分区并行），2.1×10⁵/s × 200 B ≈ 41 MB/s，对队列集群很轻，单分片内按租户并行；成本是峰值容量；
2. **摊平（smear）**：API 允许 `notAfter = fireAt + slack`，调度器在窗口内按任务 id 哈希均匀打散，或装载进时间轮时加入确定性抖动 `jitter = hash(jobId) % slack`；需要调用方同意；
3. **公平 + 优先级**：到期任务按 (tenant, fireAt) 进多个队列，每个租户有速率配额，老任务（lateness 大）优先（EDF：最早截止优先），一个租户的突发不拖慢其他租户的「准时」；
4. **背压**：分发能力暂时不足则积压，指标 `dispatch_lag` 告警，不要丢弃，也不要无限放大内存。
