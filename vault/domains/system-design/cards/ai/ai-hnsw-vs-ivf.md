---
id: ai-hnsw-vs-ivf
node: ai.vector-search
type: qa
---
## Q
HNSW vs IVF for a vector index: how does each search, and what pushes you from HNSW to IVF(+PQ)?

## A
- **HNSW**: multi-layer graph of neighbors; search greedily descends from sparse top layers to the dense bottom. Best recall/latency at query time and supports incremental inserts — but the graph lives in **RAM**, roughly (vector + neighbor links) per point.
- **IVF**: cluster the space (k-means); search only the `nprobe` closest clusters. Cheaper memory, and with **product quantization** vectors compress ~10–50x, enabling billion-scale and disk-based serving — at some recall cost.

Switch when memory, not latency, is the binding constraint (typically ≥ hundreds of millions of vectors).

## Q zh
向量索引的 HNSW vs IVF：每个搜索如何工作，什么将你从 HNSW 推向 IVF(+PQ)？

## A zh
- **HNSW**：邻居的多层图；搜索贪婪地从稀疏顶层下降到密集底层。查询时最好的召回/延迟并支持增量插入 — 但图形存在于 **RAM** 中，大致每个点（向量+邻居链接）。
- **IVF**：聚类空间（k-means）；仅搜索 `nprobe` 个最接近的集群。更廉价的内存，以及使用 **product quantization** 向量压缩 ~10–50x，启用十亿规模和基于磁盘的服务 — 以一定的召回成本。

当内存而不是延迟是限制条件时切换（通常 ≥ 数亿个向量）。
