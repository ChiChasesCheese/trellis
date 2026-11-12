---
slug: path-sum-ii
---
## Q
**LC 113 路径总和 II**｜Medium

找出二叉树中所有从根到叶子、节点值之和等于 `targetSum` 的路径。

## A
**一句话。** DFS 回溯：沿途维护共享路径和剩余值，到叶子且恰好为 `0` 时拷贝一份，离开节点时弹出。

```python
def path_sum(root, target_sum):
    res, path = [], []

    def dfs(node, rest):
        if node is None:
            return
        path.append(node.val)
        rest -= node.val
        if not node.left and not node.right and rest == 0:
            res.append(path[:])   # 拷贝，path 之后还会变
        dfs(node.left, rest)
        dfs(node.right, rest)
        path.pop()                # 回溯

    dfs(root, target_sum)
    return res
```

**复杂度。** 时间 `O(n·h)`，空间 `O(h)`。

**易错点。**
- 只判 `rest == 0` 不判叶子：`[1,2]`、目标 `1` 会收下 `[1]`，应为 `[]`。
- 收集时 `res.append(path)` 不拷贝：回溯后全变成空列表。
- 因 `rest < 0` 剪枝：节点值有负数，`[-2,null,-3]`、目标 `-5` 会漏掉。

**追问。**
- 只问是否存在（LC 112）？：不需要 `path`，叶子处判断相等，左右 `or` 短路。
- 路径不必从根开始（LC 437）？：沿 DFS 维护前缀和哈希表，`O(n)`。

**同模式。** LC 112 路径总和、LC 257 二叉树的所有路径、LC 437 路径总和 III、LC 129 求根到叶子节点数字之和
