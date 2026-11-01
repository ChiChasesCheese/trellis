---
slug: populating-next-right-pointers-in-each-node-ii
---
## Q
**LC 117 填充每个节点的下一个右侧节点指针 II**｜Medium

给定一个二叉树（不一定是完美二叉树），每个节点有 `val`、`left`、`right` 和 `next` 四个字段。填充每个节点的 `next` 指针，让它指向其下一个右侧节点；如果找不到下一个右侧节点，则设为 `NULL`。初始状态下所有 `next` 都是 `NULL`。树中节点数在 `[0, 6000]`，`-100 <= Node.val <= 100`。例：`root = [1,2,3,4,5,null,7]` → 每层按 `next` 连起来是 `1 -> #`、`2 -> 3 -> #`、`4 -> 5 -> 7 -> #`；`root = []` → `[]`。进阶：只能使用常量级额外空间；使用递归也符合要求，隐式栈空间不计入。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二叉树层序遍历（level order）；把每一层相邻节点连成链表。

**一句话。** 一层一层处理：收集当前层的所有节点，相邻两个连上 `next`，再收集下一层。

**识别。** 「同一层从左到右的下一个节点」就是层序遍历里相邻的两项；树不是完美的，所以不能靠父子关系推出 `next`，必须按层收集。

**推导。** 对每个节点向右找同层的邻居没有直接办法。层序遍历天然把同层节点放在一起：用列表保存当前层，相邻两项 `a, b` 令 `a.next = b`，最右边的节点保持 `None`；下一层由当前层每个节点的非空孩子按顺序拼出，顺序保持从左到右。

```python
class Node:                                    # LeetCode 已提供，这里列出便于对照
    def __init__(self, val: int = 0, left: "Node | None" = None,
                 right: "Node | None" = None, next: "Node | None" = None) -> None:
        self.val, self.left, self.right, self.next = val, left, right, next


def connect(root: Node | None) -> Node | None:
    level = [root] if root else []                 # 当前层，从左到右
    while level:
        for a, b in pairwise(level):               # 同层相邻节点相连；最右节点的 next 保持 None
            a.next = b
        level = [child for node in level for child in (node.left, node.right) if child]   # 下一层：按顺序展开孩子
    return root
```

运行：`[1,2,3,4,5,null,7]` 各层按 `next` 读出 `[[1], [2, 3], [4, 5, 7]]`，其中 `5.next` 是 `7`；`[]` 返回 `None`；单节点 `[1]` 返回 `[[1]]`。

**复杂度。** 时间 `O(n)`，空间 `O(w)`（`w` 为最大层宽，最坏 `O(n)`）。

**拓展优化。**
- 进阶要求常量空间：上一层的 `next` 已经连好，可以当作链表横向遍历，同时用哑节点（dummy）把下一层串起来，不再需要列表：

```python
def connect_o1(root: Node | None) -> Node | None:
    head = root                                    # 当前层最左边的节点
    while head:
        dummy = tail = Node()                      # 下一层的哑头，tail 指向已串好的最后一个
        node = head
        while node:                                # 沿着当前层已连好的 next 横向走
            for child in (node.left, node.right):
                if child:
                    tail.next = child              # 把孩子接到下一层链表末尾
                    tail = child
            node = node.next
        head = dummy.next                          # 下一层最左边的节点；没有则结束
    return root
```

**易错点。**
- 套用完美二叉树（LC 116）的写法 `node.right.next = node.next.left`：示例里 `3` 没有左孩子，`5.next` 会被设成 `None` 而不是 `7`；一般二叉树要沿 `next` 往右找到第一个有孩子的节点。
- 层序收集时不能把 `None` 孩子放进下一层，否则 `pairwise` 会把 `None` 当作节点去连接，抛 `AttributeError`。
- 直接写 `level = [root]` 而不判空：`root = None` 时 `node.left` 抛 `AttributeError`。

**同模式。** LC 116 填充每个节点的下一个右侧节点指针、LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 637 二叉树的层平均值。
