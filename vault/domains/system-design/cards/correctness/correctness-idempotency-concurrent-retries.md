---
id: correctness-idempotency-concurrent-retries
node: correctness.idempotency
type: qa
---
## Q
Two requests with the same idempotency key arrive concurrently (client timeout fired while the original was still running). What must the server do?

## A
- The key insert's **unique constraint** makes exactly one request the winner; the loser must NOT run the operation.
- The loser either **waits** for the winner's result or returns **409/425 "in progress"** with Retry-After — never a second execution, never an error implying the payment failed.
- Key record needs a state machine (`started` → `succeeded`/`failed`) so a crash mid-operation leaves a detectable `started` row for recovery, instead of a key that permanently blocks or silently double-charges.
- The check-then-act must be a single atomic insert — a read-then-insert race is exactly the double-charge you built this to prevent.

## Q zh
两个请求用同一个幂等性 key 并发到达（客户端超时重试而原始请求仍在运行）。服务器必须做什么？

## A zh
- key 的 **unique 约束**让恰好一个请求胜出；败方绝对不能执行操作。
- 败方要么**等待**赢方结果，要么返回 **409/425 "in progress"** 加 Retry-After — 绝不能二次执行，绝不能返回表示支付失败的错误。
- key 记录需要状态机（`started` → `succeeded`/`failed`），这样操作中间崩溃留下可检测的 `started` 行用于恢复，而不是永久阻塞或无声重复的 key。
- 检查-执行必须是单个原子插入 — 读-后插入竞态正是你构造幂等性来防止的重复扣款。
