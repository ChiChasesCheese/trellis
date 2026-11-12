---
slug: path-sum
---
## Q
**LC 112 路径总和**｜Easy

二叉树 `root` 和整数 `targetSum`，判断是否存在从根到**叶子**的路径，节点值之和等于 `targetSum`。

## A
**一句话。** 自顶向下 DFS 带着「还差多少」，只在叶子上检查差值是否为 `0`。

```python
def has_path_sum(root, target_sum):
    if root is None:
        return False            # 空树没有根到叶子的路径
    remain = target_sum - root.val
    if root.left is None and root.right is None:
        return remain == 0      # 必须是叶子
    return (has_path_sum(root.left, remain)
            or has_path_sum(root.right, remain))
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 不检查叶子：`root=[1,2]`、`targetSum=1`，根值已够但不是叶子，应为 `false`。
- 用 `remain < 0` 剪枝：值可为负，`[-2,null,-3]`、`-5` 会被误剪，应为 `true`。
- 空树返回 `true`：`[]`、`0` 应为 `false`。

**追问。**
- 要返回所有路径（LC 113）？：DFS 维护 `path`，到叶子且差值为 `0` 时拷贝入答案，返回前弹出。
- 路径不必从根开始（LC 437）？：改用前缀和哈希表。

**同模式。** LC 113 路径总和 II、LC 437 路径总和 III、LC 129 求根节点到叶节点数字之和、LC 257 二叉树的所有路径
