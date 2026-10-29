---
id: uth-storage-btree-3-leaf-links
node: storage.btree
type: qa
step: 3
---
## Q
**范围扫描：叶子链表还是回头找父节点**｜InnoDB · MySQL 8.4 / SQLite · 3.54

`WHERE id BETWEEN a AND b`（范围扫描）找到起点后，怎么顺着往后读？InnoDB 和 SQLite 的做法一样吗？

## A
**背景。** 整行都在叶子层，范围扫描只需要从起点所在的叶子页，一页一页读到终点。问题是：读完一页，怎么找到下一页？

**结构。** InnoDB 把同一层的页用 `FIL_PAGE_PREV` / `FIL_PAGE_NEXT` 连成双向链表，读完一页直接跳到下一页。SQLite 的 b-tree 页没有兄弟指针：游标读完叶子的最后一格，就 `moveToParent` 回到父页，再进下一个子页（`btreeNext`）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 208">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">InnoDB: 叶子页双向链表</text>
<rect x="13" y="22" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="44" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<rect x="97" y="22" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="128" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<rect x="181" y="22" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="212" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<rect x="265" y="22" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="296" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<line x1="75" y1="30" x2="91" y2="30" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="97,30 91.0,33.0 91.0,27.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="97" y1="38" x2="81" y2="38" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="75,38 81.0,35.0 81.0,41.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="159" y1="30" x2="175" y2="30" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="181,30 175.0,33.0 175.0,27.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="181" y1="38" x2="165" y2="38" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="159,38 165.0,35.0 165.0,41.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="243" y1="30" x2="259" y2="30" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="265,30 259.0,33.0 259.0,27.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="265" y1="38" x2="249" y2="38" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="243,38 249.0,35.0 249.0,41.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SQLite: 读完叶子, 回父页再下行</text>
<rect x="110" y="94" width="120" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="110.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">父页</text>
<rect x="13" y="154" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="44" y="170.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<line x1="128" y1="118" x2="44" y2="154" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="97" y="154" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="128" y="170.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<line x1="156" y1="118" x2="128" y2="154" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="181" y="154" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="212" y="170.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<line x1="184" y1="118" x2="212" y2="154" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="265" y="154" width="62" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="296" y="170.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶页</text>
<line x1="212" y1="118" x2="296" y2="154" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="170" y="200" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每跨一页都要回父页一趟</text>
</svg>
```

**细节。** SQLite 表的 b-tree 数据全在叶子，内部页只存 64 位整数键。

**为什么。** 链表让范围扫描不再碰内部页；不加链表，则省掉页分裂、合并时维护相邻页指针的麻烦，代价是每跨一页都要回父页一趟。

**例题：** LC 116 填充每个节点的下一个右侧节点指针

给一棵完美二叉树（每层都填满），把每个节点的 `next` 指针指向它右边的同层节点，最右边的指向空；只能用常量额外空间。例：`[1,2,3,4,5,6,7]` 连好后第三层是 `4 -> 5 -> 6 -> 7 -> None`。

```python
class Node:
    def __init__(self, val: int = 0, left: "Node | None" = None,
                 right: "Node | None" = None, next: "Node | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right
        self.next = next

def connect(root: "Node | None") -> "Node | None":
    leftmost = root
    while leftmost and leftmost.left:
        head = leftmost
        while head:
            head.left.next = head.right
            if head.next:
                head.right.next = head.next.left
            head = head.next
        leftmost = leftmost.left
    return root
```
