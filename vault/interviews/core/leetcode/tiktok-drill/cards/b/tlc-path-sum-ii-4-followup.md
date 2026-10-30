---
id: tlc-path-sum-ii-4-followup
node: b.path-sum-ii
type: qa
step: 4
---
## Q
**LC 113 路径总和 II**｜追问

面试官接着问：（1）树退化成 `5000` 层的链，递归超限，怎么改成迭代？（2）只问是否存在这样的路径（LC 112）？（3）路径不必从根开始、不必到叶子结束（LC 437）？

## A
1. **显式栈迭代**：栈里存 `(节点, 进入前还差多少)`。弹出节点时把值加进共享的 `path`，更新 `rest`；若是叶子且 `rest == 0`，拷贝路径入答案。随后压入一个 `None` 退出标记，再压右、左孩子；孩子处理完后弹到 `None`，把 `path` 的最后一个值弹出，回溯成对出现。

```python
def path_sum_iter(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    path: list[int] = []                          # 当前根到栈顶节点的路径，共享同一个列表
    stack: list[tuple[TreeNode | None, int]] = [(root, target_sum)]   # (节点, 进入前还差多少)；节点为 None 是"退出"标记
    while stack:
        node, rest = stack.pop()
        if node is None:                          # 子树处理完毕：回溯，把这个节点移出路径
            path.pop()
            continue
        path.append(node.val)
        rest -= node.val
        if node.left is None and node.right is None and rest == 0:
            res.append(path[:])                   # 只有叶子且恰好用完才收：拷贝一份，path 之后还会变
        stack.append((None, 0))                   # 先压退出标记，它会在两个孩子都处理完后才被弹出
        if node.right:
            stack.append((node.right, rest))
        if node.left:
            stack.append((node.left, rest))       # 后压的先弹：左子树先走，结果与递归写法同序
    return res
```

例 1 → `[[5, 4, 11, 2], [5, 8, 4, 5]]`，5000 层的链在默认递归上限下也能返回；先压右孩子后压左孩子，结果顺序与递归版一致。
2. **是否存在。** 不需要 `path` 和回溯，找到就返回，三行递归：

```python
def has_path_sum(root: TreeNode | None, target_sum: int) -> bool:
    if root is None:
        return False
    if root.left is None and root.right is None:
        return root.val == target_sum              # 叶子：恰好用完
    rest = target_sum - root.val
    return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)   # or 短路：找到就停
```

3. **任意起点终点（LC 437）。** 沿 DFS 维护前缀和计数表 `{前缀和: 次数}`：到达一个节点时，以它为终点的合法路径数等于 `计数表[当前前缀和 - 目标]`；进入节点时加一，离开时减一（回溯）。`O(n)`。

**Python 提醒**：`res.append(path)` 追加的是同一个列表对象，之后回溯会把它改掉；必须 `res.append(path[:])` 或 `list(path)` 拷贝。
