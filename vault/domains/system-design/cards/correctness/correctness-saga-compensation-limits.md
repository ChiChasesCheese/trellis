---
id: correctness-saga-compensation-limits
node: correctness.saga
type: qa
---
## Q
"On failure, just run the compensations." What three realities make saga compensation harder than a rollback?

## A
- **Compensation is semantic undo, not rollback**: a refund is a new transaction (fees, records, latency), and some actions are **non-compensatable** — you can't un-send a wire or un-ship a package. Order steps so the *pivot* (point of no return) comes after everything retriable, e.g. authorize card early, **capture last**.
- **Compensations can fail too** — they must be idempotent and retried forever (or page a human); there is no compensation for the compensation.
- **No isolation**: other transactions saw the intermediate state (lost update, dirty read). Countermeasures: *semantic locks* (mark rows `PENDING`), reordering, or commutative operations.

## Q zh
"故障时，就跑补偿。" saga 补偿比回滚难在哪三个现实？

## A zh
- **补偿是语义撤销，不是回滚**：退款是新交易（手续费、记录、延迟），有些操作**不可补偿** — 你不能取消汇出或取消发货。排序步骤让*转折点*（不可逆点）在所有可重试之后，如早期授权卡、**最后交割**。
- **补偿也可能失败** — 必须幂等和永远重试（或告警人工）；补偿的补偿不存在。
- **无隔离**：其他交易看到中间状态（丢失更新、脏读）。对策：*语义锁*（标记行 `PENDING`）、重排序，或交换律操作。
