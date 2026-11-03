---
id: hi-pt-tt-idempotent-transfer-5-atomic-check
node: tt.lld.tt-idempotent-transfer.points
type: qa
step: 5
---
## Q
**幂等转账服务 · 余额检查与扣款原子**｜必会 · 出自：幂等转账服务 › 深入 3

先读余额再写账本，两步之间别的转账可能把钱转走。怎么保证原子？热点账户怎么办？

## A
**本例。** 用 `_money` 锁把检查加记账放进一个临界区。
**生产。** 同一事务内条件更新 `UPDATE wallet SET balance = balance - x WHERE id = ? AND balance >= x`，受影响行数 0 即不足；或 `SELECT ... FOR UPDATE`，多账户按 ID 排序加锁防死锁。
**热点。** 按账户路由到单一分区串行处理，或用分片追加加快照的账本。
