---
id: tlc-maximum-product-of-splitted-binary-tree-4-followup
node: b.maximum-product-of-splitted-binary-tree
type: qa
step: 4
---
## Q
**LC 1339 分裂二叉树的最大乘积**｜追问

面试官接着问：（1）要返回应该删的是哪条边（切下来的子树根）？（2）链形树 `50000` 层，递归会怎样，怎么改成迭代？（3）输入是 N 叉树，或者直接给 `parent[]` 数组？

## A
1. **返回切点**：收集 `(子树和, 子树根)`，对 `s * (total - s)` 取最大的那一项；这个节点与它的父亲之间的边就是要删的边：

```python
def best_cut_node(root: TreeNode | None) -> TreeNode:
    cuts: list[tuple[int, TreeNode]] = []       # (子树和, 子树根)

    def dfs(node: TreeNode | None) -> int:
        if node is None:
            return 0
        s = node.val + dfs(node.left) + dfs(node.right)
        cuts.append((s, node))
        return s

    total = dfs(root)
    return max(cuts, key=lambda c: c[0] * (total - c[0]))[1]
```

2. **深链与迭代**：递归深度等于树高，链形树 `50000` 层会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`。迭代写法：显式栈做一次先序，记下每个节点的父亲下标；先序序列里子的下标大于父的下标，所以倒序遍历时子先于父，把子树和累加到父亲上即可，不需要真正的后序：

```python
def max_product_stack(root: TreeNode | None) -> int:
    MOD = 10**9 + 7
    order: list[TreeNode] = []                  # 先序（父在子前）
    parent: list[int] = []                      # parent[i]：order[i] 的父结点在 order 里的下标
    stack: list[tuple[TreeNode, int]] = [(root, -1)]
    while stack:
        node, p = stack.pop()
        idx = len(order)
        order.append(node)
        parent.append(p)
        for child in (node.left, node.right):
            if child:
                stack.append((child, idx))
    sums = [node.val for node in order]         # sums[i]：以 order[i] 为根的子树和
    for i in range(len(order) - 1, 0, -1):      # 倒着走：子一定先于父，累加到父上
        sums[parent[i]] += sums[i]
    total = sums[0]
    return max(s * (total - s) for s in sums[1:]) % MOD
```

3. **N 叉树 / `parent[]` 数组**：思路完全一样。给的是 `parent[]` 且保证 `parent[i] < i` 时，连树都不用建，直接倒序累加。

**Python 提醒**：`max(..., key=lambda ...)` 返回的是使 `key` 最大的**元素**（这里是 `(子树和, 子树根)` 元组），不是 `key` 的值；要最大值本身就直接对表达式取 `max`。
