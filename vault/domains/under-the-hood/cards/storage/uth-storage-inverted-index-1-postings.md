---
id: uth-storage-inverted-index-1-postings
node: storage.inverted-index
type: qa
step: 1
---
## Q
**倒排索引：词 → 有序文档号列表**｜Lucene · 10.5

搜索 `kafka AND timing` 时，Lucene 怎么找到同时含两个词的文档？文档号列表怎么存才不占地方？

## A
**结构。** 倒排索引（inverted index）：每个词（term）对应一个升序的文档号列表（postings）。多词 AND = 对几个有序列表求交集。

**细节。**

- 存的不是文档号，而是相邻差值（delta），每 256 个一块，按块内最大差值的位宽打包（frame of reference）；Lucene 10.4 起块大小由 128 改成 256。
- 块里的文档足够稠密时，改存位图（bitset）更省，写入器按占用空间二选一；连续的整块只记 0 位宽。

**为什么。** 列表有序所以差值小，位宽远小于 32 位；求交集只需双指针，不用全部展开。

**对应 LeetCode：** LC 349 两个数组的交集 · LC 88 合并两个有序数组
