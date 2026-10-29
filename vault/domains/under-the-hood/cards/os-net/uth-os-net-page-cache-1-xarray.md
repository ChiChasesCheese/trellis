---
id: uth-os-net-page-cache-1-xarray
node: os-net.page-cache
type: qa
step: 1
---
## Q
**读文件为什么第二次很快**｜Linux · 页缓存 · 内核 7.3

一个文件的页缓存在内核里怎么存？按偏移找某一页是什么复杂度？

## A
**结构。** 每个文件（inode）有一个 `address_space`，它的 `i_pages` 是一棵 XArray，键是页在文件里的页号。

**细节。**

- XArray 是基数树（radix tree）的继任者，每层 6 位，每个节点 64 个槽（`XA_CHUNK_SHIFT`）
- 按页号查找沿树走几层，深度约 log64(页数)，查找可以用 RCU 免锁
- `read()` 先查这棵树，命中就从内存拷贝，不碰磁盘

**为什么。** 页号稠密且连续，比哈希表省内存，还能高效取“下一页”，预读用得上。

**对应 LeetCode：** LC 208 实现 Trie（前缀树） · LC 211 添加与搜索单词
