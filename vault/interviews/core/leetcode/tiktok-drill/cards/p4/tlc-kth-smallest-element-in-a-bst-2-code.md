---
id: tlc-kth-smallest-element-in-a-bst-2-code
node: p4.kth-smallest-element-in-a-bst
type: qa
step: 2
---
## Q
**LC 230 二叉搜索树中第 K 小的元素**｜写出 Python 实现

BST 有 `n` 个节点，`1 <= k <= n <= 10^4`，节点值在 `[0, 10^4]`。返回第 `k` 小的值，树可能退化成链。

## A
**思路。** 递归中序：先递归左子树；左边已经数到第 `k` 个就直接把答案一路返回；否则数当前节点（`k` 减一），减到 `0` 返回它的值；还没到就递归右子树。

```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    def dfs(node: TreeNode | None) -> int | None:
        nonlocal k
        if node is None:
            return None
        if (found := dfs(node.left)) is not None:   # 左子树里已经数到第 k 个：一路返回，不再往下走
            return found
        k -= 1                                      # 递归返回的顺序就是升序：数当前节点
        if k == 0:
            return node.val
        return dfs(node.right)

    result = dfs(root)
    if result is None:
        raise ValueError("k 超过节点数")
    return result
```

运行：`[3,1,4,null,2]`、`k=1` → `1`；`[5,3,6,2,4,null,null,1]`、`k=3` → `3`；`10^4` 个节点的右链（值 `0` 到 `9999`），调高递归上限后 `k=10000` → `9999`，`k=1` → `0`；`10^4` 个节点的左链（值递减），`k=1` 在默认递归上限下抛 `RecursionError`。

**复杂度。** 时间 `O(h + k)`；空间 `O(h)`，是递归栈，链状树上为 `O(n)`。

**写法要点。** `nonlocal k` 让内层函数直接把 `k` 当计数器递减，不用额外变量；`:=` 把左子树的返回值存下来并判断是否找到，找到就立刻返回，提前终止整条递归；用 `None` 当「还没找到」的哨兵，因为节点值可以是 `0`，所以要写 `is not None` 而不是靠真值；循环结束仍没返回说明 `k > n`，用 `raise` 比返回魔法值 `-1` 更明确（题目保证不会发生）。深度超过约 `1000` 要 `sys.setrecursionlimit`，或用「追问」卡的迭代版。
