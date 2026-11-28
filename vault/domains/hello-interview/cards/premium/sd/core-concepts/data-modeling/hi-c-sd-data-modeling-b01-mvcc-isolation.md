---
id: hi-c-sd-data-modeling-b01-mvcc-isolation
node: sd.core-concepts.data-modeling.beyond
type: qa
step: 1
---
## Q
**数据建模 · 关系型库的"强一致"到底保护了什么**｜拓展 · 加分
说"支付用 ACID 所以不会重复扣款"为什么不够严谨？默认隔离级别下库存仍可能超卖吗？

## A
- **ACID 保证事务内的原子性，但不自动保证业务不变量。** PostgreSQL 默认隔离级别是读已提交（Read Committed）。两个事务都先读出库存为 1，再各自减一，会出现丢失更新（lost update），库存变成 -1 或超卖。
- **解法：** 原子更新 `UPDATE ... SET stock = stock - 1 WHERE stock > 0`，检查和修改在同一条语句里；或用 `SELECT ... FOR UPDATE` 加行锁；或乐观锁（版本号，写入时比较）；或升到可串行化（Serializable）并准备重试失败的事务。
- **支付防重复：** 还要靠业务上的唯一约束（订单号或幂等键唯一），而不是只靠事务。
- **面试价值：** 说出"ACID 是工具，不变量要自己设计到语句或约束里"。
