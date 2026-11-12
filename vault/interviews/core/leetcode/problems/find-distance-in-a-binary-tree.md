---
slug: find-distance-in-a-binary-tree
---
## Q
**LC 1740 找到二叉树中的距离**｜Medium

二叉树中结点值唯一，求值为 `p` 与值为 `q` 的结点之间路径上的边数。

## A
**一句话。** 路径必经最近公共祖先 LCA，先递归找 LCA，再分别算 LCA 到 `p`、`q` 的深度相加。

```python
def find_distance(root, p, q):
    def lca(node):
        if not node or node.val in (p, q):
            return node
        l, r = lca(node.left), lca(node.right)
        return node if l and r else l or r

    def down(node, t):       # node 到值 t 的边数，找不到 -1
        if node.val == t:
            return 0
        for ch in node.left, node.right:
            if ch and (d := down(ch, t)) >= 0:
                return d + 1
        return -1

    top = lca(root)
    return down(top, p) + down(top, q)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 只加深度不扣 LCA：`p=6, q=2` 的深度和是 `4`，正确答案是 `2`。
- `down` 找不到时返回 `0` 而不是 `-1`：把「没找到」当成「就是这个结点」，走错子树。

**追问。**
- 树很深、递归爆栈？：迭代遍历记下父节点和深度，让较深者往上爬直到相遇，步数即距离。
- 同一棵树查询很多对？：预处理倍增表，每次 `O(log n)`。

**同模式。** LC 236 二叉树的最近公共祖先、LC 235 二叉搜索树的最近公共祖先、LC 863 二叉树中所有距离为 K 的结点、LC 2096 从二叉树一个结点到另一个结点的每步方向
