---
id: hi-c-sd-vector-databases-n05-hnsw-structure
node: sd.deep-dives.vector-databases.notes
type: qa
step: 5
---
## Q
**向量数据库 · HNSW 的结构：向量版的跳表**｜摘要 · 必会

HNSW 是什么思路？它的多层图怎么构造？

## A
- **类比跳表（skip list）：** 普通链表找元素要逐个扫，O(n)；跳表在其上加"快车道"层，高层只保留随机的一小部分元素，查找时先在高层快速前进，快越过目标就下一层，得到 O(log n)。
- **HNSW**（Hierarchical Navigable Small World）：把这个思想用到图上。每个向量是一个节点；插入时找出最相似的向量并建立边，所以"Taylor Swift"会和"Beyoncé""Ed Sheeran"相连，不是人工连的，而是向量在空间里本来就近。
- **性质：** 沿边可以从任何向量走到相似向量；相似的向量之间通常有短路径。
- **分层：** 最底层（第 0 层）包含全部向量，各自连着近邻；每个向量有一定概率被提升到更高层：第 0 层有百万节点，第 1 层可能几万，第 2 层几百。高层的点是"长距离连接"，让你快速跨越空间。
- **地位：** 生产中最流行的算法，只记一个就记它。
