---
id: storage-index-leftmost-prefix
node: storage.relational.indexing
type: qa
---
## Q
You have a composite B-tree index on `(tenant_id, created_at)`. Which of these can use it efficiently: (a) `WHERE tenant_id = ?`, (b) `WHERE created_at > ?`, (c) `WHERE tenant_id = ? AND created_at > ?` — and why?

## A
(a) and (c). A composite index is sorted by the **leftmost column first**; entries for one `tenant_id` are contiguous, and within them sorted by `created_at`.

(b) alone can't seek — matching rows are scattered across every tenant's section, forcing a full index/table scan.

Ordering rule: put **equality columns first, then the range column**; a range on an earlier column stops the index being useful for later columns.

## Q zh
你有一个 `(tenant_id, created_at)` 上的复合 B-tree 索引。这些哪些能有效使用它：(a) `WHERE tenant_id = ?`，(b) `WHERE created_at > ?`，(c) `WHERE tenant_id = ? AND created_at > ?`——为什么？

## A zh
(a) 和 (c)。复合索引按**最左列优先**排序；一个 `tenant_id` 的条目是连续的，在它们内按 `created_at` 排序。

(b) 单独不能 seek——匹配的行分散在每个 tenant 的部分，强制全索引/表扫描。

排序规则：先放**相等列，然后范围列**；在较早列上的范围会让索引对后面的列无用。
