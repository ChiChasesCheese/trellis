---
id: uth-storage-btree-3-leaf-links
node: storage.btree
type: qa
step: 3
---
## Q
**范围扫描：叶子链表还是回头找父节点**｜InnoDB · MySQL 8.4 / SQLite · 3.54

`WHERE id BETWEEN a AND b` 找到起点后，怎么顺着往后读？InnoDB 和 SQLite 的做法一样吗？

## A
**结构。** 数据都在叶子层。InnoDB 把同一层的页用 `FIL_PAGE_PREV` / `FIL_PAGE_NEXT` 连成双向链表，读完一页直接跳下一页。

**细节。**

- SQLite 的 b-tree 页没有兄弟指针：游标读完叶子的最后一格，就 `moveToParent` 回到父页，再进下一个子页（`btreeNext`）。
- SQLite 表的 b-tree 数据全在叶子，内部页只存 64 位整数键。

**为什么。** 链表让范围扫描不再碰内部页；不加链表则省掉页分裂、合并时维护相邻页指针的麻烦，代价是每跨一页都要回父页一趟。

**对应 LeetCode：** LC 116 填充每个节点的下一个右侧节点指针 · LC 173 二叉搜索树迭代器
