---
id: storage-btree-single-copy-locking
node: storage.internals.tradeoffs
type: qa
---
## Q
"In a B-tree, each key exists in exactly one place; an LSM-tree may hold several versions of it in different files." Why does this single-copy property make B-trees the comfortable substrate for *transactional* databases?

## A
Because most transaction machinery wants a stable, unique home per record:

- **Locking**: a lock manager can attach a lock to *the* place a key lives (or to a leaf-page range for range locks / next-key locking, which prevents phantoms). In an LSM, "the record" is the merged view of memtable plus several SSTables — there is no single physical location to anchor such state, so transactional LSM engines must keep locking entirely in separate in-memory structures.
- **Predictability**: reading a key costs one root-to-leaf path, always; no answer depends on how many un-compacted files exist right now. Transactional workloads (OLTP) prize this steady point-read/update latency more than raw ingest.
- **In-place update semantics**: an overwrite really replaces the old bytes, so "current value" is unambiguous without waiting on background merges.

This — not read speed alone — is a key reason the default OLTP engines (InnoDB, Postgres heap+B-tree) stay B-tree-based while LSM dominates write-heavy, simpler-consistency stores. See [[storage-btree-vs-lsm]].

## Q zh
"在 B-tree 里，每个 key 恰好存在于一个地方；LSM-tree 可能在不同文件里持有它的多个版本。"为什么这个单副本性质让 B-tree 成为*事务型*数据库舒适的底座？

## A zh
因为大多数事务机制都想要每条记录有一个稳定、唯一的家：

- **加锁**：锁管理器可以把锁挂在 key 所在的*那个*位置上（或挂在叶子页面的范围上做范围锁 / next-key locking，从而防止幻读）。在 LSM 里，"这条记录"是 memtable 加若干 SSTable 的归并视图 — 没有单一物理位置可以锚定这种状态，所以支持事务的 LSM 引擎必须把锁完全放在独立的内存结构里。
- **可预测性**：读一个 key 永远是一条根到叶的路径；答案不取决于当前有多少未 compaction 的文件。事务型负载（OLTP）看重这种平稳的点读/更新延迟胜过原始写入吞吐。
- **原地更新语义**：覆盖写真的替换了旧字节，"当前值"无需等待后台合并就毫无歧义。

这 — 而不只是读速度 — 是默认 OLTP 引擎（InnoDB、Postgres 的 heap+B-tree）坚持 B-tree、而 LSM 统治写入繁重、一致性要求更简单的存储的关键原因。见 [[storage-btree-vs-lsm]]。
