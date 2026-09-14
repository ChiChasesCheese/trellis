---
id: storage-search-deep-pagination
node: storage.search
type: qa
---
## Q
Why does `from=99000, size=20` melt a sharded search cluster when page 1 is instant, and what's the correct pattern for deep result access?

## A
Results come from distributed top-K: **every shard** must compute and return its own top `from+size` (99,020) scored docs, and the coordinator merges all of them to pick 20 — cost grows linearly with depth **multiplied by shard count**, mostly to produce results it throws away. Elasticsearch caps `from+size` at 10,000 for this reason.

Correct patterns:
- **`search_after`**: cursor on the sort values of the last hit — each shard returns only 20 docs after that key; depth-independent. (With a point-in-time snapshot so pages stay consistent.)
- For full exports, don't paginate a search engine at all — scan the source of truth ([[storage-search-not-sot]]).

## Q zh
为什么 `from=99000, size=20` 在分片搜索集群融化而页 1 是即时的，深结果访问的正确模式是什么？

## A zh
结果来自分布式 top-K：**每个分片**必须计算并返回它自己的前 `from+size`（99,020）得分文档，协调器合并所有来选 20——成本线性增长深度**乘以分片数**，主要是产生它扔掉的结果。Elasticsearch 因此限制 `from+size` 在 10,000。

正确模式：
- **`search_after`**：最后命中的排序值上的游标——每个分片仅在该键后返回 20 个文档；深度无关。（有一个点-in-时间快照所以页保持一致。）
- 对于完整导出，根本不对搜索引擎分页——扫描真实来源（[[storage-search-not-sot]]）。
