---
id: hl-sd02-cancel-race
node: system-design.sd02-job-scheduler
type: qa
step: 12
---
## Q
`cancel` 与「到期出轮」同时发生怎么办？单写者设计里竞态怎么处理？

## A
同一分片的所有命令（cancel、到期出轮）由**同一个单写线程**串行处理，所以不存在数据竞争，只有**业务竞态**：
- cancel 先到 → `CANCELLED`，任务从轮中摘除（O(1)，job 表记录了它在哪个 slot 的哪个链表）；
- 到期先发生 → 任务已是 `DISPATCHING`，cancel 返回 `TOO_LATE`（幂等：重复 cancel 同样返回）。

分布式角度：cancel 必须路由到同一分片 leader，并与触发使用同一个日志序列。确认取消后不会再有新触发，已在途的交付除外（可选让下游再检查）。

一句话：单写者把竞态变成顺序，谁先进入日志谁定义语义。
