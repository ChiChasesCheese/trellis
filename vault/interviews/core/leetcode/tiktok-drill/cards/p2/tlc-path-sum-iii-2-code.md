---
id: tlc-path-sum-iii-2-code
node: p2.path-sum-iii
type: qa
step: 2
---
## Q
**LC 437 路径总和 III**｜写出 Python 实现

二叉树（结点数 `0..1000`，值在 `[-10^9, 10^9]`，可为负）和整数 `targetSum`（`-1000..1000`）。数出结点值之和为 `targetSum` 的向下路径条数，路径可从任意结点开始、在任意结点结束。要求 `O(n)`。

## A
**思路。** DFS 时维护一张「根到当前结点这条链上的前缀和 → 次数」的表。到结点 `b` 时，答案加上表里 `前缀(b) - targetSum` 的次数，再把 `前缀(b)` 记入表；离开 `b` 时撤销。表一开始放 `{0: 1}`，代表空前缀。用递归 DFS，进入时加入、返回前撤销，回溯自然落在函数返回处。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> int:
    prefix: Counter[int] = Counter({0: 1})       # 当前根到结点链上：前缀和 -> 出现次数

    def dfs(node: TreeNode | None, total: int) -> int:   # total：根到 node 父亲的和
        if node is None:
            return 0
        total += node.val                        # 根到 node 的和
        count = prefix[total - target_sum]       # 有多少个祖先前缀和恰好差 target_sum
        prefix[total] += 1                       # 进入：把 node 的前缀和加入当前链
        count += dfs(node.left, total) + dfs(node.right, total)
        prefix[total] -= 1                       # 离开：撤销，别的分支看不到这条链
        return count

    return dfs(root, 0)
```

运行：`root=[10,5,-3,3,2,null,11,3,-2,null,1], targetSum=8` → `3`，`root=[5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum=22` → `3`，`root=[], targetSum=0` → `0`，`root=[1,-1,1,-1,1], targetSum=0` → `2`，`1000 个结点的单链，值全 0，targetSum=0` → 默认递归上限下抛 `RecursionError`，调高上限后 `500500`。

**复杂度。** 时间 `O(n)`：每个结点进入、离开各一次，字典操作 `O(1)`；空间 `O(n)`：递归深度 `O(h)`（1000 结点的链会触到默认递归上限），`Counter` 里撤销后键仍保留，最坏有 `n` 个不同的前缀和。

**写法要点。** `Counter` 对不存在的键返回 `0` 且**不插入**，所以 `prefix[total - target_sum]` 可以直接读；`Counter({0: 1})` 一步完成播种；`total` 作为参数向下传，不用在返回时再减；`prefix[total] += 1` 与 `prefix[total] -= 1` 夹住两个子树的递归，回溯就是这一对语句；函数返回值累加左右子树的路径数，不需要 `nonlocal`。
