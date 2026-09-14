---
id: storage-hash-index-limits
node: storage.relational.indexing
type: qa
---
## Q
A hash index answers `WHERE id = ?` in O(1) — seemingly better than a B-tree's O(log n). Why is the B-tree still the default index almost everywhere? Name what hashing structurally cannot do.

## A
Hashing destroys **key order** — entries land wherever the hash function scatters them. That forfeits everything a sorted structure gives for free:

- **Range queries** (`BETWEEN`, `>`, date windows) — a hash index can't enumerate "keys from A to B" without scanning everything.
- **Prefix matches and sorted output** — no `LIKE 'abc%'`, no serving `ORDER BY` from the index.
- **Composite leftmost-prefix reuse** — a hash of `(a, b)` answers only the exact pair, never `a` alone.

Meanwhile the B-tree's O(log n) is tiny in practice — 3–4 page reads with the upper levels cached — so hashing's win is marginal. Hash indexes earn their place where equality is truly all there is: in-memory KV stores, hash-partitioned lookups, join hash tables built at query time.

## Q zh
Hash 索引以 O(1) 回答 `WHERE id = ?` — 看起来比 B-tree 的 O(log n) 更好。为什么 B-tree 仍然几乎在所有地方都是默认索引？说出哈希在结构上做不到的事。

## A zh
哈希摧毁了 **key 的有序性** — 条目落在哈希函数把它们打散到的任何位置。这就放弃了有序结构免费赠送的一切：

- **范围查询**（`BETWEEN`、`>`、日期窗口）— hash 索引不扫描全部就无法枚举"从 A 到 B 的 key"。
- **前缀匹配和有序输出** — 做不了 `LIKE 'abc%'`，也不能用索引直接满足 `ORDER BY`。
- **复合索引的 leftmost-prefix 复用** — 对 `(a, b)` 做哈希只能回答精确的二元组，永远无法单独回答 `a`。

与此同时 B-tree 的 O(log n) 在实践中很小 — 3–4 次页面读取，且上层页面都在缓存里 — 所以哈希的优势微乎其微。Hash 索引在"真的只有等值查询"的场景才配得上位置：内存 KV 存储、按哈希分区的查找、查询时临时构建的 join 哈希表。
