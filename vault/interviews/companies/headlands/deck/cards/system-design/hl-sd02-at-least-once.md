---
id: hl-sd02-at-least-once
node: system-design.sd02-job-scheduler
type: qa
step: 22
---
## Q
调度器的「至少一次」从哪来？在「交付成功」与「写 Fired」之间崩溃会怎样？为什么不能先写 Fired 再交付？

## A
顺序：到期 → 状态 `DISPATCHING` → 异步交付 → 下游确认 → 追加 `Fired`，都由单写线程完成。

- 在交付成功与 `Fired` 写入日志之间崩溃：恢复后日志里没有 `Fired`，任务仍是 `SCHEDULED` / `DISPATCHING`，所以**会再交付一次**，这就是 at-least-once；
- 如果先写 `Fired` 再交付：崩溃会**丢**触发，违反 I4（不丢）。所以顺序必须是「交付成功后再记 Fired」。

因此下游必须用 `jobId`（与 attempt 无关）去重：幂等键。
