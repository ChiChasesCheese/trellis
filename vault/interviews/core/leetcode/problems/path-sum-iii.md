---
slug: path-sum-iii
---
## Q
**LC 437 路径总和 III**｜Medium

二叉树中求结点值之和等于 `targetSum` 的向下路径条数，路径不必从根开始、不必在叶子结束。

## A
**一句话。** 前缀和哈希：向下路径即根到当前结点链上的子数组，数祖先前缀和等于 `当前和 - target` 的个数，进入加入、离开撤销。

```python
def path_sum(root, target_sum):
    prefix = Counter({0: 1})     # 当前链上：前缀和 -> 次数

    def dfs(node, total):
        if node is None:
            return 0
        total += node.val
        count = prefix[total - target_sum]
        prefix[total] += 1       # 进入
        count += dfs(node.left, total)
        count += dfs(node.right, total)
        prefix[total] -= 1       # 离开，撤销
        return count

    return dfs(root, 0)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 忘了播种 `{0: 1}`：从根出发的路径数不到，`root=[1]`、`targetSum=1` 得 `0`，应为 `1`。
- 离开时忘了撤销：左子树的前缀和泄漏到右子树，`root=[0,1,3]`、`targetSum=2` 得 `1`，应为 `0`。
- 用滑动窗口：值含负数，窗口和不单调。

**追问。**
- 树很深、递归会超限？：改成显式栈，进出时同样加入和撤销前缀和。
- 路径可以向上再向下？：换成后序 DFS，在每个结点合并左右子树。

**同模式。** LC 560 和为 K 的子数组、LC 112 路径总和、LC 113 路径总和 II、LC 974 和可被 K 整除的子数组
