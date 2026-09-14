---
id: storage-multicolumn-vs-bitmap-and
node: storage.relational.indexing
type: qa
---
## Q
Query: `WHERE a = ? AND b = ?`. You could build one composite index on `(a, b)` or rely on two existing single-column indexes on `a` and on `b`. How does the database actually use the two separate indexes, and when is the composite worth building anyway?

## A
With two single-column indexes, Postgres-style engines do a **bitmap index scan**: scan each index separately, build a bitmap of candidate row locations per index, **AND the bitmaps**, then fetch the surviving heap pages. It works, and it composes across arbitrary predicates the composite can't anticipate.

Build the composite when:

- **Both predicates together are selective but each alone is not** — bitmap-AND still pays to scan every entry matching `a = ?` and every entry matching `b = ?` before intersecting; the composite seeks straight to the tiny `(a, b)` slice.
- You need **sorted output** (`ORDER BY b` within `a`) or an index-only scan — bitmaps lose row order and can't cover.
- The query is hot: one index traversal beats two scans plus an intersection every time.

Keep the separate indexes when filter combinations are ad hoc — one composite per combination is a write-cost explosion ([[storage-index-write-cost]]).

## Q zh
查询：`WHERE a = ? AND b = ?`。你可以建一个 `(a, b)` 复合索引，或依赖已有的 `a`、`b` 两个单列索引。数据库实际上如何使用这两个独立索引，什么情况下仍值得建复合索引？

## A zh
有两个单列索引时，Postgres 风格的引擎会做 **bitmap index scan**：分别扫描每个索引，为每个索引构建候选行位置的 bitmap，**把 bitmap 做 AND**，然后取回幸存的堆页面。这可行，而且能在复合索引无法预料的任意谓词组合间自由组合。

以下情况建复合索引：

- **两个谓词合起来选择性高但单独都不高** — bitmap-AND 仍要在求交之前扫完所有匹配 `a = ?` 的条目和所有匹配 `b = ?` 的条目；复合索引直接定位到很小的 `(a, b)` 切片。
- 你需要**有序输出**（`a` 内按 `ORDER BY b`）或 index-only scan — bitmap 会丢失行序，也无法覆盖查询。
- 查询很热：一次索引遍历每次都胜过两次扫描加一次求交。

当过滤条件组合是临时随意的时，保留独立的单列索引 — 为每种组合建一个复合索引是写成本的爆炸（[[storage-index-write-cost]]）。
