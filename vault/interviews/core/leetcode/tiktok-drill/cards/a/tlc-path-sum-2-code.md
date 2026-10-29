---
id: tlc-path-sum-2-code
node: a.path-sum
type: qa
step: 2
---
## Q
**LC 112 路径总和**｜写出 Python 实现

二叉树 `root`（结点数 `0..5000`，值 `-1000..1000`，可为负）和整数 `targetSum`。判断是否存在一条从根到某个叶子的路径，其结点值之和恰好等于 `targetSum`。

## A
**思路。** 栈里存「结点 + 走到该结点后还差多少」。弹出一个结点，如果它是叶子并且还差 `0`，就找到了；否则把它的孩子连同更新后的剩余量压栈。空树直接返回 `False`，栈空还没找到也返回 `False`。

```python
def has_path_sum(root: TreeNode | None, target_sum: int) -> bool:
    if root is None:
        return False                   # 空树没有任何根到叶子的路径
    stack = [(root, target_sum - root.val)]   # (结点, 走到这里后还差多少)
    while stack:                       # 迭代 DFS：树可以退化成 5000 层的链，递归会爆栈
        node, remain = stack.pop()
        if node.left is None and node.right is None and remain == 0:
            return True                # 必须是叶子，并且恰好凑够
        for child in (node.right, node.left):
            if child:
                stack.append((child, remain - child.val))
    return False
```

运行：`root=[5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum=22` → `True`，`root=[1,2,3], targetSum=5` → `False`，`root=[], targetSum=0` → `False`，`root=[1,2], targetSum=1（根不是叶子）` → `False`，`root=[-2,null,-3], targetSum=-5（负数）` → `True`，`5000 个结点的单链，值全为 1，targetSum=5000` → `True`。

**复杂度。** 时间 `O(n)`：每个结点最多入栈、出栈一次；空间 `O(h)`：栈里最多存一条根到叶的链上的待探索结点，平衡树 `O(log n)`，退化成链 `O(n)`。

**写法要点。** `stack = [(root, target_sum - root.val)]` 把根的处理合进初始化，循环里每个结点都已经扣过自己的值；`node.left is None and node.right is None` 精确表达「叶子」（用 `not node.left` 也行，但要避免和 `val == 0` 的结点混淆——这里比较的是结点引用，不会混淆）；`for child in (node.right, node.left)` 一次遍历两个孩子，`if child:` 过滤空；元组解包 `node, remain = stack.pop()`。递归写法 `return rec(l, t - v) or rec(r, t - v)` 利用 `or` 短路，找到后不再探索另一侧，但会受递归深度限制。
