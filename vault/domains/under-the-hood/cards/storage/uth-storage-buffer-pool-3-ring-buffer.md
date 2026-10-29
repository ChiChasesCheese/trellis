---
id: uth-storage-buffer-pool-3-ring-buffer
node: storage.buffer-pool
type: qa
step: 3
---
## Q
**大表扫描只用一个小环形缓冲**｜PostgreSQL · 17 / 18

PostgreSQL 顺序扫描一张比缓冲池还大的表，会不会把池里的热数据冲掉？

## A
**结构。** 不会。大表的顺序扫描改用一个小的环形缓冲（ring buffer）：只在这几个缓冲区里循环复用，淘汰也在环内完成。

**细节。**

- 触发条件：表大于 `shared_buffers` 的 1/4（`NBuffers / 4`）。
- 环大小：顺序扫描 256 KB（17 及之前；18 起再加上异步 I/O 并发所需的空间），`VACUUM` 2 MB，批量写入（如 `COPY`）16 MB。

**为什么。** 比 InnoDB 的中点 LRU 更直接：扫描页干脆不进全局的淘汰池。

**对应 LeetCode：** LC 622 设计循环队列
