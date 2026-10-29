---
id: tlc-maximum-product-of-splitted-binary-tree-4-followup
node: a.maximum-product-of-splitted-binary-tree
type: qa
step: 4
---
## Q
**LC 1339 分裂二叉树的最大乘积**｜追问

面试官接着问：（1）要返回应该删的是哪条边（切下来的子树根）？（2）输入是 N 叉树，或者直接给 `parent[]` 数组？（3）递归写法怎么写，为什么这里不能用？分别怎么改。

## A
1. **返回切点**：枚举时取下标最大化目标，再回到 `order[i]`；这个节点与它的父亲之间的边就是要删的边：

```python
def best_cut_node(root: TreeNode | None) -> TreeNode:
    order: list[TreeNode] = []
    parent: list[int] = []
    stack: list[tuple[TreeNode, int]] = [(root, -1)]
    while stack:
        node, p = stack.pop()
        idx = len(order)
        order.append(node)
        parent.append(p)
        for child in (node.left, node.right):
            if child:
                stack.append((child, idx))
    sums = [node.val for node in order]
    for i in range(len(order) - 1, 0, -1):
        sums[parent[i]] += sums[i]
    total = sums[0]
    best = max(range(1, len(order)), key=lambda i: sums[i] * (total - sums[i]))
    return order[best]
```

2. **N 叉树 / `parent[]` 数组**：思路完全一样。给的是 `parent[]` 且保证 `parent[i] < i` 时，连树都不用建，直接倒序累加。
3. **递归写法**：后序返回子树和，把每个子树和存进列表。短，但链形树深度 `50000` 会触发 `RecursionError`；先写递归说明思路，再说明为什么要改迭代。

**Python 提醒**：`max(..., key=lambda i: ...)` 返回的是使 `key` 最大的**元素**（这里是下标），不是 `key` 的值；要最大值本身就直接对表达式取 `max`。
