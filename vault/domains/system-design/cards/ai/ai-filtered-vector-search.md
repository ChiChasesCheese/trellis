---
id: ai-filtered-vector-search
node: ai.vector-search
type: qa
---
## Q
"Top-10 similar docs WHERE tenant_id = 42": why does naive post-filtering break this query, and what do engines do instead?

## A
**Post-filter** (ANN top-k, then apply the predicate) fails when the filter is selective: if tenant 42 owns 0.1% of vectors, the top-50 ANN hits may contain **zero** matching docs — you return too few or garbage. Cranking k up to compensate destroys latency.

Alternatives:

- **Filter-aware traversal**: evaluate the predicate *during* HNSW/IVF search, only scoring passing vectors (Qdrant, pgvector w/ filtering, etc.) — works until the filter is so selective the graph becomes disconnected.
- **Partitioning**: one index (or namespace) per tenant/category — the right answer for multitenancy, which is also an **isolation** requirement, not just recall ([[ai-corpus-freshness]] notes the authorization-leak risk).
- **Brute-force fallback**: for tiny filtered sets, exact scan beats ANN.

## Q zh
"前 10 个相似文档 WHERE tenant_id = 42"：为什么朴素的后过滤会破坏此查询，引擎如何处理？

## A zh
**后过滤**（ANN top-k 然后应用谓词）在过滤器是选择性的时失败：如果租户 42 拥有 0.1% 的向量，前 50 个 ANN 命中可能包含 **零个** 匹配文档 — 你返回太少或垃圾。提高 k 来补偿会破坏延迟。

替代方案：

- **过滤器感知遍历**：在 HNSW/IVF 搜索 *期间* 评估谓词，只对通过的向量评分（Qdrant、pgvector 带过滤等）— 工作到过滤器非常选择性导致图形断开连接。
- **分区**：每个租户/类别一个索引（或命名空间）— 多租户的正确答案，这也是 **隔离** 需求，不仅仅是召回（[[ai-corpus-freshness]] 注意到授权泄露风险）。
- **蛮力回退**：对于微小的过滤集合，精确扫描优于 ANN。
