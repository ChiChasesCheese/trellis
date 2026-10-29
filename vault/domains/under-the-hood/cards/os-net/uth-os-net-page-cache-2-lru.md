---
id: uth-os-net-page-cache-2-lru
node: os-net.page-cache
type: qa
step: 2
---
## Q
**页缓存的淘汰：两条 LRU 链表**｜Linux · 经典 LRU 与 MGLRU · 内核 6.12

页缓存满了该丢哪页？只读一遍的大文件为什么冲不掉热数据？

## A
**结构。** 文件页挂在活跃和不活跃两条 LRU 链表上（`LRU_ACTIVE_FILE` 与 `LRU_INACTIVE_FILE`），回收优先从不活跃链表的尾部下手。

**细节。**

- 新页先进不活跃链表，被第二次访问（`folio_mark_accessed`）才升入活跃链表
- 只读一遍的流式数据没有机会升级，直接从不活跃端淘汰
- 6.1 起有多代 LRU（MGLRU，`CONFIG_LRU_GEN`）：页按年龄分到最多 4 代（`MAX_NR_GENS`）

**为什么。** 单条 LRU 会被一次大文件扫描冲掉所有热页；“访问两次才算热”是便宜的抗扫描办法。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
