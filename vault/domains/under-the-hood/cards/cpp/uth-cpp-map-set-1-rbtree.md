---
id: uth-cpp-map-set-1-rbtree
node: cpp.map-set
type: qa
step: 1
---
## Q
**map 与 set 底下是什么**｜C++ · libstdc++ 16

`std::map` / `std::set` 为什么遍历出来是有序的，查找是 O(log n)？

## A
**背景。** 想要一份“随时有序、又能快速插入和查找”的数据。有序数组二分查找快，但插入要把后面的元素整体后移，是 O(n)；链表插入快，找一个值却要从头走。折中是二叉搜索树（binary search tree）：每个节点的左边都比它小，右边都比它大，找一个值每走一步就排除一半。

**结构。** 红黑树（red-black tree）是能自动保持平衡的二叉搜索树：每个节点存父、左、右三个指针和一位颜色（红或黑）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<rect x="6" y="6" width="84" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="48" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">头节点</text>
<text x="48" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最左 最右 个数</text>
<line x1="159.421" y1="37.5561" x2="110.579" y2="72.4439" stroke="currentColor" stroke-width="1"/>
<line x1="180.579" y1="37.5561" x2="229.421" y2="72.4439" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="92.545" y1="90.65" x2="72.455" y2="119.35" stroke="currentColor" stroke-width="1"/>
<line x1="107.455" y1="90.65" x2="127.545" y2="119.35" stroke="currentColor" stroke-width="1"/>
<line x1="232.545" y1="90.65" x2="212.455" y2="119.35" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="247.455" y1="90.65" x2="267.545" y2="119.35" stroke="currentColor" stroke-width="1"/>
<circle cx="170" cy="30" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="170" y="34.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="100" cy="80" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="100" y="84.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="240" cy="80" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2" stroke-dasharray="4 3"/>
<text x="240" y="84.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<circle cx="65" cy="130" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="65" y="134.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="135" cy="130" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="135" y="134.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="205" cy="130" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="205" y="134.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="275" cy="130" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="275" y="134.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<circle cx="208" cy="24" r="6" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="218" y="28" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">红</text>
<circle cx="254" cy="24" r="6" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="264" y="28" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">黑</text>
<text x="212" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">蓝线: 查 5</text>
<rect x="60" y="160" width="28" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="74" y="175.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<line x1="88" y1="171" x2="94" y2="171" stroke="currentColor" stroke-width="1"/>
<polygon points="94,171 88.0,173.7 88.0,168.3" fill="currentColor"/>
<rect x="94" y="160" width="28" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="108" y="175.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="122" y1="171" x2="128" y2="171" stroke="currentColor" stroke-width="1"/>
<polygon points="128,171 122.0,173.7 122.0,168.3" fill="currentColor"/>
<rect x="128" y="160" width="28" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="142" y="175.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="156" y1="171" x2="162" y2="171" stroke="currentColor" stroke-width="1"/>
<polygon points="162,171 156.0,173.7 156.0,168.3" fill="currentColor"/>
<rect x="162" y="160" width="28" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="176" y="175.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="190" y1="171" x2="196" y2="171" stroke="currentColor" stroke-width="1"/>
<polygon points="196,171 190.0,173.7 190.0,168.3" fill="currentColor"/>
<rect x="196" y="160" width="28" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="210" y="175.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="224" y1="171" x2="230" y2="171" stroke="currentColor" stroke-width="1"/>
<polygon points="230,171 224.0,173.7 224.0,168.3" fill="currentColor"/>
<rect x="230" y="160" width="28" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="244" y="175.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<line x1="258" y1="171" x2="264" y2="171" stroke="currentColor" stroke-width="1"/>
<polygon points="264,171 258.0,173.7 258.0,168.3" fill="currentColor"/>
<rect x="264" y="160" width="28" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="278" y="175.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="170" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">中序遍历 1 2 3 … 7: 自然有序</text>
</svg>
```

**细节。**

- 例：图里放着 1 到 7，查 5 只走 4、6、5 三步（蓝线）；中序遍历（先左、再自己、再右）读出来正好是 1 2 3 … 7，所以遍历有序
- 树根旁的头节点还记着最左、最右节点和元素个数，所以 `begin()` 是 O(1)
- 插入、删除后靠旋转（局部改几个指针）和变色保持平衡，最长路径不超过最短路径的 2 倍
- Java 的 `TreeMap` 也是红黑树

**为什么。** 普通二叉搜索树按顺序插入会退化成一条链；红黑树比 AVL 树平衡得松，插入最多只需两次旋转，适合频繁插入删除；比哈希表多了有序和范围查询。

**例题：** LC 98 验证二叉搜索树（同类：LC 235 二叉搜索树的最近公共祖先）

给一棵二叉树，判断它是不是合法的二叉搜索树：每个节点的左子树全部严格小于它，右子树全部严格大于它。例：`[2,1,3]` 是，`[5,1,4,null,null,3,6]` 不是。解法的依据就是：中序遍历读出来必须严格递增。

```python
class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val, self.left, self.right = val, left, right

def is_valid_bst(root: TreeNode | None) -> bool:
    stack: list[TreeNode] = []
    node = root
    prev_val: int | None = None
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev_val is not None and node.val <= prev_val:
            return False
        prev_val = node.val
        node = node.right
    return True
```
