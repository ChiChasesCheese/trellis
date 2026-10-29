---
id: uth-storage-query-exec-2-external-sort
node: storage.query-exec
type: qa
step: 2
---
## Q
**外部排序：切段排序，再 k 路归并**｜PostgreSQL · 18

`ORDER BY` 的数据远大于 `work_mem` 时，PostgreSQL 怎么排序？一次最多同时归并几路？

## A
**结构。** 外部排序（external sort）：每攒满 `work_mem`（默认 4 MB）的元组，就在内存里快排成一段有序的 run 写进临时文件；最后把所有 run 做 k 路归并。

**细节。**

- 归并路数 = `work_mem / (2 × 8 KB + 256 KB)`，下限 6、上限 500；默认 4 MB 得 15 路。
- 15 版之前用多相归并（polyphase），15 起改成平衡归并：多相归并为磁带设计，现在每个“磁带”只是几 KB 缓冲。

**坑。** 路数封顶 500：路数太高，CPU 缓存效应更差，多付一趟 I/O 反而更快。

**对应 LeetCode：** LC 23 合并 K 个升序链表 · LC 912 排序数组
