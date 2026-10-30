---
id: tlc-find-distance-in-a-binary-tree-2-code
node: p4.find-distance-in-a-binary-tree
type: qa
step: 2
---
## Q
**LC 1740 找到二叉树中的距离**｜写出 Python 实现

二叉树（结点数 `[1, 10^4]`，值唯一，`0 <= Node.val <= 10^9`）与两个存在于树中的值 `p`、`q`，返回二者之间路径的边数。树可能是 `10^4` 层的单链。

## A
**思路。** 先用递归找 `p`、`q` 的最近公共祖先：空或命中 `p` / `q` 就返回自己，左右各返回一个结点说明当前结点就是 LCA，否则返回非空的一边。再写一个 `down(node, target)`，从 LCA 往下找 `target` 并返回边数，找不到返回 `-1`。答案是两次 `down` 之和。

```python
def find_distance(root: TreeNode | None, p: int, q: int) -> int:
    def lca(node: TreeNode | None) -> TreeNode | None:
        if node is None or node.val in (p, q):
            return node                        # 空，或者碰到 p / q 本身：向上报告
        left, right = lca(node.left), lca(node.right)
        return node if left and right else left or right   # 两边各有一个：自己就是 LCA

    def down(node: TreeNode, target: int) -> int:
        if node.val == target:
            return 0
        for child in (node.left, node.right):
            if child and (d := down(child, target)) >= 0:
                return d + 1                   # 在这个孩子的子树里找到了
        return -1                              # 这棵子树里没有 target

    top = lca(root)                            # p、q 的最近公共祖先
    return down(top, p) + down(top, q)         # 路径 = LCA 到 p + LCA 到 q
```

运行：示例树上 `p=5, q=0` → `3`，`p=5, q=7` → `2`，`p=5, q=5` → `0`，`p=6, q=2` → `2`；单结点树 `p=q=7` → `0`；`10^4` 个结点的左链上，调高递归上限后 `p=0, q=9999` → `9999`，`p=5000, q=9999` → `4999`；默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n)`：`lca` 一次加两次 `down`，各最多 `n` 个结点；空间 `O(h)`，是递归栈。

**写法要点。** `node.val in (p, q)` 一次判断两个目标；`return node if left and right else left or right` 一行表达三种情况（两边都有、只有一边、都没有），依赖结点对象为真、`None` 为假；`(d := down(child, target)) >= 0` 用海象运算符把递归结果存下来再比较，省一次重复调用；`for child in (node.left, node.right)` 统一处理左右；链状树深度可达 `10^4`，要 `sys.setrecursionlimit` 或用「追问」卡的迭代版。
