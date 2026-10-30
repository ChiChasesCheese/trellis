---
id: tlc-core-path-sum-iii
node: p3.path-sum-iii
type: qa
---
## Q
**LC 437 路径总和 III**｜Medium · LC TikTok 热度 41/100（近 30 天） · 近一年被问：美国 3 次、国内 3 次 · CodeTop 国内累计 7 次 · 最近 2026-10-07（国内 CodeTop） · 也在：Amazon、LeetCode Hot 100

给二叉树的根结点 `root` 和整数 `targetSum`，求结点值之和等于 `targetSum` 的**路径**条数。路径不必从根开始、不必在叶子结束，但方向必须向下（只能从父结点走到子结点）。

约束：结点数在 `[0, 1000]`，`-10^9 <= Node.val <= 10^9`，`-1000 <= targetSum <= 1000`。

例：`root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8` → `3`（`5→3`、`5→2→1`、`-3→11`）；`root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把「树上的向下路径」看成「根到当前结点这条链上的子数组」：用前缀和哈希表数「有多少个祖先前缀和等于 `当前和 - targetSum`」，进入结点时加入、离开时撤销。`O(n)`。

**识别。** 「和等于目标值的**连续**片段」是前缀和 + 哈希的标志（同 LC 560 和为 K 的子数组）；树上向下路径恰好是一条链上的连续片段，只是要在 DFS 里维护「当前链」的前缀和表。值可以为负，所以滑动窗口 / 双指针不能用（不单调）。`n ≤ 1000` 允许 `O(n^2)`，但 `O(n)` 更好，面试官期待你说出前缀和。

**推导。** 暴力：以每个结点为起点向下 DFS 累加，命中就计数，`O(n·h)`，最坏链 `O(n^2)`。浪费在于相邻起点的路径大量重叠、反复求和。洞察：路径 `a→…→b` 的和 = `前缀(b) - 前缀(a的父)`，其中前缀是根到结点的和。所以到达结点 `b` 时，只需问「当前链上有几个前缀和等于 `前缀(b) - targetSum`」——一次哈希查询。哈希表只保留**当前根到 `b` 的链**：进入结点 `+1`，离开 `-1`（回溯），别的分支才不会误用。初始放入 `{0: 1}` 代表「空前缀」，让从根开始的路径也能被数到。

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

**复杂度。** 时间 `O(n)`：每个结点进入、离开各一次，字典操作 `O(1)`；空间 `O(n)`：递归深度 `O(h)`，`Counter` 里撤销后键仍保留，最坏有 `n` 个不同的前缀和。

**易错点。**
- 忘了播种 `{0: 1}`：从根出发的路径数不到。`root=[1]`, `targetSum=1` 答案是 `1`，漏播种得 `0`；例 2（`22`）有两条从根出发的路径 `5→4→11→2`、`5→8→4→5`，漏播种只剩 `1`（正确 `3`）。
- 忘了离开时撤销：左子树的前缀和泄漏到右子树。`root=[0,1,3]`，`targetSum=2`，正确 `0`，不撤销得 `1`（右结点 `3` 误用了左结点残留的前缀和 `1`）。
- 用滑动窗口：值含负数，窗口和不单调。
- 递归深度：1000 结点的单链深度就是 1000，CPython 默认递归上限约 1000，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见追问）。

**追问。**
- 返回所有路径本身：同样的 DFS，另维护一个 `path` 栈；因为要列出起点，哈希表改成 `前缀和 → 下标列表`。
- 路径可以向上向下（任意两点间）：这就是树上的「任意路径和」，需要换成后序 DFS 在每个结点合并左右子树，不再是前缀和。
- N 叉树或「只数以叶子结尾」：前缀和哈希不变，只是遍历孩子列表；以叶子结尾则在叶子处才计数。
- 不想递归（树很深）：显式栈，同一个结点压两次，第二次是「离开」标记，用来撤销前缀和：
```python
def path_sum_stack(root: TreeNode | None, target_sum: int) -> int:
    count = 0
    prefix: Counter[int] = Counter({0: 1})   # 当前根到结点链上：前缀和 -> 出现次数
    stack: list[tuple[TreeNode | None, int, bool]] = [(root, 0, False)]
    while stack:                             # 迭代 DFS：进入时加入前缀和，离开时撤销
        node, total, leaving = stack.pop()
        if node is None:
            continue
        if leaving:
            prefix[total] -= 1               # 回溯：别的分支看不到这条链
            continue
        total += node.val                    # 根到 node 的和
        count += prefix[total - target_sum]  # 有多少个祖先前缀和恰好差 target_sum
        prefix[total] += 1
        stack.append((node, total, True))
        stack.append((node.right, total, False))
        stack.append((node.left, total, False))
    return count
```

**同模式。** LC 560 和为 K 的子数组（一维版）、LC 112 / 113 路径总和 I / II、LC 523 连续的子数组和、LC 974 和可被 K 整除的子数组。
