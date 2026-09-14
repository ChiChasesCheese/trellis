---
id: storage-partial-expression-index
node: storage.relational.indexing
type: qa
---
## Q
A 500M-row `jobs` table has 2k rows in `status='pending'` that a worker polls constantly. What index do you build, and what related index type fixes `WHERE lower(email) = ?`?

## A
A **partial index**: `CREATE INDEX ON jobs (run_at) WHERE status = 'pending'`.

- Size tracks the **2k live rows**, not 500M — it stays fully cached, and entries are removed as jobs complete, so the hot queue index never grows with history.
- Cheaper writes too: rows that don't satisfy the predicate are never indexed at all.
- The planner only uses it when it can prove the query's predicate **implies** the index predicate, so the constant must match (`status = 'pending'`, not a bound parameter in some engines).

For `lower(email)`, build an **expression index** — `CREATE INDEX ON users (lower(email))`. The index stores the computed value, so the query's expression must match the indexed one *textually*; that also makes it the standard way to enforce case-insensitive uniqueness.

## Q zh
一个 500M 行的 `jobs` 表有 2k 行 `status='pending'` 的行被 worker 不断轮询。你建什么索引，什么相关索引类型修复 `WHERE lower(email) = ?`？

## A zh
一个**部分索引**：`CREATE INDEX ON jobs (run_at) WHERE status = 'pending'`。

- 大小跟踪**2k 活行**，不是 500M——它保持完全缓存，条目随着任务完成被移除，所以热队列索引永远不与历史增长。
- 更便宜的写：不满足谓词的行根本不被索引。
- 计划器只在它能证明查询谓词**隐含**索引谓词时使用它，所以常数必须匹配（`status = 'pending'`，在某些引擎中不是绑定参数）。

对于 `lower(email)`，建一个**表达式索引**——`CREATE INDEX ON users (lower(email))`。索引存储计算值，所以查询的表达式必须**文本上**匹配被索引的那个；这也使它成为强制不区分大小写唯一性的标准方式。
