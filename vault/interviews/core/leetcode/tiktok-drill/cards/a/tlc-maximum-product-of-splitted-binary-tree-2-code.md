---
id: tlc-maximum-product-of-splitted-binary-tree-2-code
node: a.maximum-product-of-splitted-binary-tree
type: qa
step: 2
---
## Q
**LC 1339 分裂二叉树的最大乘积**｜写出 Python 实现

二叉树（节点数 `2 ~ 50000`，值 `1 ~ 10000`），删掉一条边得到两棵子树，求它们节点值之和的乘积的最大值，结果对 `10^9 + 7` 取模。注意树可能退化成长度 `50000` 的链。

## A
**思路。** 先用显式栈做一次先序遍历，记下每个节点的父亲下标。倒序遍历这个先序序列（子必在父之后出现，所以倒序时子先于父），把每个节点的子树和累加到父亲上，`sums[0]` 就是整棵树的和 `total`。最后对所有非根节点计算 `s * (total - s)` 取最大，再取模。

```python
def max_product(root: TreeNode | None) -> int:
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
    # 先在精确整数上取最大，最后才取模
    return max(s * (total - s) for s in sums[1:]) % MOD
```

运行：`[1,2,3,4,5,6]` → `110`，`[1,null,2,3,4,null,null,5,6]` → `90`，`[2,3,9,10,7,8,6,5,4,11,1]` → `1025`，`[1,1]` → `1`，`10 个节点的链，值都是 10000` → `499999986`。

**复杂度。** 时间 `O(n)`：每个节点入栈出栈一次，倒序累加一遍，再枚举一遍；空间 `O(n)`（`order`、`parent`、`sums`、栈）。

**写法要点。** 用两个并行列表 `order` / `parent` 代替递归栈和字典：先序序列的倒序天然满足「子在父前」，累加只需一个 `for i in range(len-1, 0, -1)`，不需要真正的后序遍历。栈里放 `(节点, 父亲下标)` 元组，入栈时就带上父亲位置。`max(生成器表达式)` 不建中间列表。`% MOD` 放在 `max` 外面，利用 Python 整数不溢出，先精确比较再取模。
