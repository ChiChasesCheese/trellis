---
id: hi-pt-delayed-payment-scheduler-4-claim-lease
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 4
---
## Q
**延迟支付调度服务 · 抢占到期任务与租约**｜必会 · 出自：延迟支付调度服务 › 整体设计

每个分片上有多个扫描器同时找到期的预约。怎样让一条预约只被一个执行者拿到，且执行者崩溃后不会卡死？

## A
**要点。** 抢占语句：`UPDATE ... SET status='EXECUTING', lease_until=now()+60s WHERE id IN (SELECT ... WHERE (SCHEDULED 且已到期) OR (EXECUTING 且租约已过期) ORDER BY execute_at LIMIT 200 FOR UPDATE SKIP LOCKED)`。

**为什么。** SKIP LOCKED 让多个扫描器互不阻塞；租约过期后任务可被重新抢占，崩溃不会卡死。
