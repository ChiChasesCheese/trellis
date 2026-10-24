---
id: tlc-path-sum-ii-2-code
node: b.path-sum-ii
type: qa
step: 2
---
## Q
**LC 113 路径总和 II**｜写出 Python 实现

二叉树根节点 `root`（节点数 `0..5000`，值 `-1000..1000`）与整数 `targetSum`。返回所有根到叶子、节点值之和等于 `targetSum` 的路径，每条路径是节点值列表。注意树可能是 5000 层的链。

## A
**思路。** 迭代 DFS。栈里存 `(节点, 进入前还差多少)`。弹出节点时把值加进共享的 `path`，更新 `rest`；若是叶子且 `rest == 0`，拷贝路径入答案。随后压入一个 `None` 退出标记，再压右、左孩子；孩子处理完后弹到 `None`，把 `path` 的最后一个值弹出。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> list[list[int]]:
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

**运行。** 例 1 → `[[5, 4, 11, 2], [5, 8, 4, 5]]`；`[1,2,3], 5` → `[]`；`[1,2], 0` → `[]`；`None, 0` → `[]`；`[1], 1` → `[[1]]`；`[-2,null,-3], -5` → `[[-2, -3]]`；5000 层的链也能正常返回。

**复杂度。** 时间 `O(n + k·h)`（遍历 `n` 个节点，`k` 条命中路径各拷贝 `O(h)`）；空间 `O(h)`，不含输出。

**写法要点。** 栈元素用 `(节点, rest)`，`rest` 随栈走，比单独维护一个"当前和"变量更不易在回溯时出错；`path[:]` 是浅拷贝，元素是整数，足够；用 `None` 作退出标记，让"进入时 `append`、离开时 `pop`"在没有递归的情况下成对出现；先压右孩子后压左孩子，保证左子树先出栈，结果顺序与常见递归写法一致。
