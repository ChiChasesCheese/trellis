---
id: storage-index-selectivity
node: storage.relational.indexing
type: qa
---
## Q
There is a B-tree index on the column, but `EXPLAIN` shows a sequential scan. Give the two distinct reasons a planner *chooses* not to use it, and the one that means it *cannot*.

## A
**Chooses not to (cost):**
- **Low selectivity** — the predicate matches a large fraction of rows. An index scan costs ~1 random heap I/O per matching row; a seq scan reads pages sequentially. Above roughly **5–10% of the table** the seq scan wins, so `WHERE status = 'active'` on a 90%-active table correctly ignores the index.
- **Bad or stale statistics** — the planner's row estimate is wrong (skewed values, no `ANALYZE` after a bulk load, correlated columns it assumes are independent). The plan is optimal *for the estimate*, not for reality.

**Cannot (non-sargable predicate):** the indexed column is wrapped or coerced — `WHERE lower(email) = ?`, `WHERE created_at::date = ?`, `LIKE '%foo'`, or an implicit type cast on the column side. The index is sorted on the raw column, so no seek range exists.

## Q zh
有一个 B-tree 索引在列上，但 `EXPLAIN` 显示顺序扫描。给出计划器**选择**不使用它的两个不同原因，以及意味着它**不能**的那个。

## A zh
**选择不使用（成本）：**
- **低选择性**——谓词匹配表的大部分行。索引扫描成本约每个匹配行一次随机 heap I/O；顺序扫描按顺序读页。大约**表的 5–10%** 以上顺序扫描胜出，所以在 90% 活跃的表上的 `WHERE status = 'active'` 正确地忽略索引。
- **坏的或过时的统计**——计划器的行估计错误（偏斜值、bulk load 后没有 `ANALYZE`、它假设独立的相关列）。计划对**估计是最优**的，不是对现实。

**不能（非 sargable 谓词）：**被索引列被包装或强制——`WHERE lower(email) = ?`、`WHERE created_at::date = ?`、`LIKE '%foo'` 或列一侧隐式类型转换。索引按原始列排序，所以不存在 seek 范围。
