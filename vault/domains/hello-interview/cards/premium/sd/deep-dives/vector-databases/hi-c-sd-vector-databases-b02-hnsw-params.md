---
id: hi-c-sd-vector-databases-b02-hnsw-params
node: sd.deep-dives.vector-databases.beyond
type: qa
step: 2
---
## Q
**向量数据库 · HNSW 的三个参数与召回调节**｜拓展 · 加分

HNSW 有哪些可调参数？分别影响什么？

## A
- **M（每个节点的连接数）：** 越大图越稠密，召回更好，内存与建索引时间更多。
- **efConstruction 管建图质量：** efConstruction（建索引时的候选队列大小）：越大建出的图质量越高、召回上限越高，建索引更慢，只在构建时生效。
- **efSearch（查询时的候选队列大小）：** 越大探索越多、召回越高、延迟越长，可以在查询时随时调整，是线上调召回与延迟的主要旋钮。
- **pgvector 默认：** `m = 16`、`ef_construction = 64`、`hnsw.ef_search = 40`。
- **调参方法：** 在评估集上固定召回目标，先调 efSearch；不够再提高 M 与 efConstruction 重建。
- **和 IVF 对照：** efSearch 对应 IVF 的 nprobe，都是"查询时多探索一点"的旋钮。
