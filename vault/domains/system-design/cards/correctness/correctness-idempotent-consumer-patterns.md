---
id: correctness-idempotent-consumer-patterns
node: correctness.idempotency
type: qa
---
## Q
Beyond an idempotency-key table, name three ways to make a mutation safe to apply twice — and the classic operation that is NOT naturally idempotent.

## A
- **Natural idempotency**: absolute writes — `SET status = 'shipped'`, upsert by primary key. Applying twice converges to the same state.
- **Conditional write / compare-and-set**: `UPDATE ... WHERE version = 41` or `WHERE status = 'pending'` — the second application matches zero rows.
- **Dedup by processed-event id**: consumer records `(consumer, event_id)` with a unique constraint in the **same transaction** as its state change.

Not naturally idempotent: **relative updates** — `balance = balance + 100`. Any increment/decrement must be guarded by one of the above.

## Q zh
除了幂等性 key 表，说出三种让变更安全应用两次的方法 — 以及不天然幂等的经典操作。

## A zh
- **天然幂等性**：绝对写 — `SET status = 'shipped'`，按主键 upsert。应用两次收敛到同一状态。
- **条件写 / compare-and-set**：`UPDATE ... WHERE version = 41` 或 `WHERE status = 'pending'` — 第二次应用匹配零行。
- **按处理事件 id 去重**：consumer 在与状态改变**同一事务**内记录 `(consumer, event_id)` 加 unique 约束。

不天然幂等：**相对更新** — `balance = balance + 100`。任何增减都必须由上述之一守卫。
