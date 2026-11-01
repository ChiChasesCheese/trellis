---
id: tlc-tops-path-sum-iii-0-whole
node: trees.path-sum-iii
type: qa
---
## Q
**LC 437 路径总和 III**｜Medium · 全公司热度第 372 名 · Hot 100、LeetCode 75

给定二叉树的根节点 `root` 和整数 `targetSum`，求节点值之和等于 `targetSum` 的**路径**数目。路径不需要从根节点开始，也不需要在叶子节点结束，但方向必须向下（只能从父节点到子节点）。节点数在 `[0, 1000]`，`-10^9 <= Node.val <= 10^9`，`-1000 <= targetSum <= 1000`。例：`root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8` → `3`（`5→3`、`5→2→1`、`-3→11`）；`root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22` → `3`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 前缀和 + 哈希表（LC 560）搬到树上，带回溯的 DFS。

**一句话。** 根到当前节点的链就是一个数组：当前前缀和 `total`，以当前节点结尾、和为 `targetSum` 的路径数 = 这条链上前缀和等于 `total - targetSum` 的祖先个数；进入节点时登记，离开时撤销。

**识别。** 「和等于目标的**连续**片段」是前缀和加哈希的标志；树上的向下路径恰好是根链上的连续片段。值可以为负，所以不能用滑动窗口。`n <= 1000` 允许 `O(n^2)`，`O(n)` 更稳。

**推导。** 以每个节点为起点向下 DFS 累加，路径重叠大，最坏链状 `O(n^2)`。路径 `a→…→b` 的和 = `前缀(b) - 前缀(a 的父)`，所以到 `b` 时只需问「当前链上有几个前缀和等于 `前缀(b) - targetSum`」，一次哈希查询。哈希表只能保存**当前根到 `b` 的链**，所以离开节点时要撤销，别的分支才不会误用。

**简单解法。** 双重递归：外层把每个节点当起点，内层向下累减 `targetSum`，余数为 `0` 就计一条（不能提前返回，值可以为负）。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> int:
    def count_from(node: TreeNode | None, remain: int) -> int:   # 以 node 为起点的向下路径数
        if node is None:
            return 0
        remain -= node.val
        return (remain == 0) + count_from(node.left, remain) + count_from(node.right, remain)

    def dfs(node: TreeNode | None) -> int:                       # 每个节点都当一次起点
        if node is None:
            return 0
        return count_from(node, target_sum) + dfs(node.left) + dfs(node.right)

    return dfs(root)
```

时间平衡树 `O(n log n)`、链状 `O(n^2)`，`n <= 1000` 能过。

最优解：

```python
from collections import Counter

def path_sum(root: TreeNode | None, target_sum: int) -> int:
    prefix: Counter[int] = Counter({0: 1})         # 当前链上：前缀和 -> 出现次数；空前缀的和是 0

    def dfs(node: TreeNode | None, total: int) -> int:   # total：根到 node 父亲的和
        if node is None:
            return 0
        total += node.val                          # 根到 node 的和
        count = prefix[total - target_sum]         # 有多少个祖先前缀和恰好差 target_sum
        prefix[total] += 1                         # 进入：把 node 登记进当前链
        count += dfs(node.left, total) + dfs(node.right, total)
        prefix[total] -= 1                         # 离开：撤销，别的分支看不到这条链
        return count

    return dfs(root, 0)
```

运行：示例 1（`targetSum=8`）→ `3`；示例 2（`22`）→ `3`；`[]`，`0` → `0`；`[1,-1,1,-1,1]`，`0` → `2`；`[1]`，`1` → `1`。

**复杂度。** 时间 `O(n)`，每个节点进出各一次；空间 `O(n)`，递归栈和哈希表。

**拓展优化。**
- 深链输入要避免递归：把同一个节点入栈两次，第二次是「离开」标记，用来撤销前缀和。
```python
def path_sum_stack(root: TreeNode | None, target_sum: int) -> int:
    count = 0
    prefix: Counter[int] = Counter({0: 1})
    stack: list[tuple[TreeNode | None, int, bool]] = [(root, 0, False)]
    while stack:
        node, total, leaving = stack.pop()
        if node is None:
            continue
        if leaving:
            prefix[total] -= 1                     # 离开：撤销
            continue
        total += node.val
        count += prefix[total - target_sum]
        prefix[total] += 1
        stack.append((node, total, True))          # 先压「离开」标记，处理完两棵子树后才轮到它
        stack.append((node.right, total, False))
        stack.append((node.left, total, False))
    return count
```

**易错点。**
- 忘了播种 `{0: 1}`：从根出发的路径数不到。`root = [1]`，`targetSum = 1` 得 `0`，正确是 `1`。
- 离开时不撤销：左子树的前缀和泄漏到右子树。`root = [0,1,3]`，`targetSum = 2` 应为 `0`，不撤销得 `1`。
- 链状树深度 `1000` 会触到 CPython 默认递归上限约 `1000`，需调高上限或用上面的栈版。

**同模式。** LC 560 和为 K 的子数组、LC 112 路径总和、LC 113 路径总和 II、LC 974 和可被 K 整除的子数组。
