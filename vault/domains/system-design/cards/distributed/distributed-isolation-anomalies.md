---
id: distributed-isolation-anomalies
node: distributed.transactions.isolation
type: qa
---
## Q
Map the standard isolation levels to the anomaly each one newly prevents, and name the anomaly snapshot isolation still allows.

## A
| Level | Newly prevents |
|---|---|
| Read committed | Dirty reads/writes |
| Repeatable read / **Snapshot isolation** | Non-repeatable (fuzzy) reads; SI gives a consistent point-in-time snapshot |
| Serializable | Everything, incl. **write skew** and phantoms |

**Snapshot isolation still allows write skew**: two transactions read the same snapshot, make disjoint writes based on it, and jointly violate an invariant. Practical notes: Postgres defaults to read committed; Postgres "repeatable read" *is* SI; its serializable is SSI (optimistic, aborts instead of locking).

## Q zh
把标准的隔离级别和它各自新阻止的异常对应起来，并说出快照隔离仍然允许的那个异常。

## A zh
| 级别 | 新阻止的异常 |
|---|---|
| Read committed | 脏读/脏写 |
| Repeatable read / **快照隔离（Snapshot isolation）** | 不可重复（模糊）读；SI 给出一个一致的时间点快照 |
| Serializable | 所有异常，包括**写倾斜（write skew）**和幻读 |

**快照隔离仍然允许写倾斜**：两个事务读同一个快照，基于它各自做出互不相交的写入，合并之后共同违反了某个不变量。实践提示：Postgres 默认是 read committed；Postgres 的 "repeatable read" *就是* SI；它的 serializable 是 SSI（乐观，靠中止而不是加锁）。
