---
id: tlc-lowest-common-ancestor-of-a-binary-tree-iii-0-whole
node: c.lowest-common-ancestor-of-a-binary-tree-iii
type: qa
---
## Q
**LC 1650 二叉树的最近公共祖先 III**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2024-11-13（国内 CodeTop）

给定一棵二叉树中的两个节点 `p` 和 `q`，返回它们的最近公共祖先节点（LCA）。每个节点都包含其父节点的引用（指针），`Node` 有 `val`、`left`、`right`、`parent`。最近公共祖先的定义：`p` 和 `q` 的后代中既包括 `p` 又包括 `q` 的最深节点，允许一个节点是自己的后代。树中节点个数在 `[2, 10^5]`，`-10^9 <= Node.val <= 10^9`，所有 `Node.val` 互不相同，`p != q`，`p` 和 `q` 存在于树中。例：树 `[3,5,1,6,2,0,8,null,null,7,4]`，`p = 5, q = 1` → `3`；`p = 5, q = 4` → `5`（一个节点可以是自己的祖先）；树 `[1,2]`，`p = 1, q = 2` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 有父指针，两个节点各沿父链向上走，走到根就换到对方的起点继续走；两者走过的总步数相同，必然在 LCA 处相遇，就像求两个链表的相交点，`O(h)` 时间、`O(1)` 空间。

**识别。** 「有 parent 指针」把树变成了许多条向上汇合的链表，求 LCA 退化为「两条链表的第一个公共节点」（LC 160）。有这个信号就不要从根往下递归。

**推导。** 暴力：把 `p` 的所有祖先放进集合，再从 `q` 向上找第一个在集合里的，`O(h)` 时间但 `O(h)` 空间。洞察：设 `p` 到 LCA 有 `a` 步，`q` 到 LCA 有 `b` 步，LCA 到根有 `c` 步。指针 A 从 `p` 出发，走完 `p` 到根的路径后跳到 `q`；指针 B 对称。A 走到 LCA 的总步数是 `(a + c + 1) + b`，B 是 `(b + c + 1) + a`，相等，所以两者同时到 LCA。若两个节点在跳转前就相遇，那也是 LCA。

**简单解法。** 把 `p` 的祖先（含自己）收进集合，再从 `q` 向上找第一个在集合里的节点。

```python
class Node:
    def __init__(self, val: int) -> None:
        self.val = val
        self.left: Node | None = None
        self.right: Node | None = None
        self.parent: Node | None = None


def lowest_common_ancestor_set(p: Node, q: Node) -> Node:
    ancestors: set[Node] = set()
    node: Node | None = p
    while node:                                  # 收集 p 到根的整条路径（含 p）
        ancestors.add(node)
        node = node.parent
    node = q
    while node not in ancestors:                 # q 向上第一个落在 p 路径上的节点
        node = node.parent
    return node
```

`O(h)` 时间，`O(h)` 空间；已经正确，只是用了额外空间。

最优解：

```python
def lowest_common_ancestor(p: Node, q: Node) -> Node:
    a, b = p, q
    while a is not b:                            # 两个指针总步数相同，必在 LCA 相遇
        a = a.parent if a.parent else q          # 走到根之后换到对方的起点
        b = b.parent if b.parent else p
    return a
```

运行：示例 1（`p = 5, q = 1`）→ `3`，示例 2（`p = 5, q = 4`）→ `5`，示例 3（`p = 1, q = 2`）→ `1`；10 万个节点的链（`p` 是叶子、`q` 是根）→ `q` 本身，且循环无递归。

**复杂度。** 时间 `O(h)`，空间 `O(1)`。

**拓展优化。**
- 先量深度、让较深的指针先走差值，再一起向上走，每个指针只走一遍，不依赖「换起点」的技巧。

```python
def lowest_common_ancestor_depth(p: Node, q: Node) -> Node:
    def depth(node: Node) -> int:
        d = 0
        while node.parent:
            node = node.parent
            d += 1
        return d

    dp, dq = depth(p), depth(q)
    while dp > dq:                               # 把较深的节点提到同一层
        p, dp = p.parent, dp - 1
    while dq > dp:
        q, dq = q.parent, dq - 1
    while p is not q:                            # 同层后一起向上，第一个相同的就是 LCA
        p, q = p.parent, q.parent
    return p
```

**易错点。**
- 走到根不换起点、直接 `a = a.parent`：`p = 5, q = 4` 时指针走出根后变成 `None`，下一步 `None.parent` 抛 `AttributeError`。
- 用 `val` 而不是节点身份判断相遇：值互不相同时碰巧正确，值一旦可重复就会提前在错误的节点返回；这里用 `is not`。

**追问。**
- 没有 parent 指针（LC 236）：从根递归，返回左右子树里找到的目标，左右都找到则当前节点是 LCA。
- 大量查询同一棵树：预处理倍增表（binary lifting），每次查询 `O(log n)`。

**同模式。** LC 160 相交链表、LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 1676 二叉树的最近公共祖先 IV、LC 141 环形链表。
