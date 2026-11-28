---
id: hi-c-sd-postgres-n18-transactions
node: sd.deep-dives.postgres.notes
type: qa
step: 18
---
## Q
**PostgreSQL · 事务只是起点，不是一致性的全部**｜摘要 · 必会

为什么面试里说"选 PostgreSQL 因为它支持 ACID"还不够？事务本身保证什么？

## A
- **常见失误：** 只说"它是 ACID 的"，却讲不出具体怎样用它满足一致性需求。
- **事务（transaction）：** 一组要么全成功、要么全失败的操作，是一致性的基础。例：转账 `BEGIN; 扣 A; 加 B; COMMIT;`，保证不会只扣不加。
- **局限：** 事务保证单个操作序列的原子性，但多个事务并发时，仅靠事务不足以保证一致。
- **应该这样说：** 点出具体的并发风险，并说明你用哪种手段（行锁、隔离级别、乐观并发）化解。
