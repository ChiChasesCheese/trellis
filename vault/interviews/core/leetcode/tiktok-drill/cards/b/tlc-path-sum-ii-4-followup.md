---
id: tlc-path-sum-ii-4-followup
node: b.path-sum-ii
type: qa
step: 4
---
## Q
**LC 113 路径总和 II**｜追问

面试官接着问：（1）只问是否存在这样的路径（LC 112）？（2）路径不必从根开始、不必到叶子结束（LC 437）？（3）为什么不直接写递归？

## A
1. **是否存在。** 栈里只存 `(节点, rest)`，不需要 `path` 和回溯，找到就返回：

```python
def has_path_sum(root: TreeNode | None, target_sum: int) -> bool:
    stack = [(root, target_sum)] if root else []
    while stack:
        node, rest = stack.pop()
        rest -= node.val
        if not node.left and not node.right and rest == 0:
            return True
        if node.right:
            stack.append((node.right, rest))
        if node.left:
            stack.append((node.left, rest))
    return False
```

2. **任意起点终点（LC 437）。** 沿 DFS 维护前缀和计数表 `{前缀和: 次数}`：到达一个节点时，以它为终点的合法路径数等于 `计数表[当前前缀和 - 目标]`；进入节点时加一，离开时减一（回溯）。`O(n)`。
3. **递归。** 递归版只有 8 行，面试官爱看；但链状树深度可达 5000，默认递归上限是 1000，会抛 `RecursionError`。要么 `sys.setrecursionlimit`（深度太大有崩溃风险），要么像上面这样改成显式栈。

**Python 提醒**：`res.append(path)` 追加的是同一个列表对象，之后回溯会把它改掉；必须 `res.append(path[:])` 或 `list(path)` 拷贝。
