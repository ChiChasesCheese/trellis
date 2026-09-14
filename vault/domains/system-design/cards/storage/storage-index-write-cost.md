---
id: storage-index-write-cost
node: storage.relational.indexing
type: qa
---
## Q
A table has 9 indexes "just in case." Quantify what each additional index costs the write path, and how you decide which ones to drop.

## A
- Every `INSERT`/`DELETE` becomes **1 + N structure updates** — each index takes a random-ish write into a different B-tree page, plus WAL bytes for each. Insert throughput on a wide-indexed table commonly lands at a fraction of the same table with one index.
- `UPDATE` is the sharp edge in Postgres: if any **indexed** column changes (or the page has no free space), the HOT optimization is lost and the new row version must be inserted into **every** index, not just the one you touched.
- Indexes also multiply **vacuum/maintenance** work, bloat, and cache pressure — they compete with the table for buffer pool.

Drop by evidence: `pg_stat_user_indexes.idx_scan = 0` over a full business cycle (watch replicas too), plus indexes made redundant by a leftmost prefix of a wider one. Drop with `CONCURRENTLY`, and keep unique/constraint-backing indexes regardless of scan count.

## Q zh
一个表有 9 个"以防万一"的索引。量化每个额外索引对写路径的成本，你如何决定删除哪些。

## A zh
- 每个 `INSERT`/`DELETE` 变成**1 + N 个结构更新**——每个索引在不同 B-tree 页进行随机-ish 写，加上每个的 WAL 字节。在大索引表上插入吞吐通常是同一表只有一个索引的一部分。
- `UPDATE` 是 Postgres 的锋利边缘：如果任何**被索引**列改变（或页没有空闲空间），HOT 优化丢失，新行版本必须插入到**每个**索引，不只是你接触的那个。
- 索引也乘以**vacuum/维护**工作、膨胀和缓存压力——它们与表竞争缓冲池。

按证据删除：完整业务周期上的 `pg_stat_user_indexes.idx_scan = 0`（也看副本），加上由更宽索引的最左前缀冗余的索引。用 `CONCURRENTLY` 删除，无论扫描计数保留唯一/约束支持的索引。
