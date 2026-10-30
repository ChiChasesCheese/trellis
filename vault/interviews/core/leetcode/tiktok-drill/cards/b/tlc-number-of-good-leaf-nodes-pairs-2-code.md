---
id: tlc-number-of-good-leaf-nodes-pairs-2-code
node: b.number-of-good-leaf-nodes-pairs
type: qa
step: 2
---
## Q
**LC 1530 好叶子节点对的数量**｜写出 Python 实现

二叉树的根 `root`（节点数 `1..2^10`）和整数 `distance`（`1..10`）。两个叶子之间的最短路径长度 `<= distance` 就算好叶子对，返回好叶子对的数量。单链树的深度可达 `1023`。

## A
**思路。** 后序递归，`dfs(node)` 返回 `cnt[d]`：子树里距它恰好 `d` 的叶子数。叶子是 `[1, 0, …]`。内部节点把每个孩子返回的数组右移一位（距离加一），左右两个数组配对统计，再相加上报。

```python
from itertools import accumulate


def count_pairs(root: TreeNode | None, distance: int) -> int:
    ans = 0

    def dfs(node: TreeNode | None) -> list[int]:    # 返回 cnt：cnt[d] = 子树里距 node 恰好 d 的叶子数（d <= distance）
        nonlocal ans
        if node is None:
            return [0] * (distance + 1)
        if not node.left and not node.right:
            return [1] + [0] * distance             # 叶子自己距自己 0
        left = [0] + dfs(node.left)[:distance]      # 孩子子树的叶子，距 node 都多 1；超过 distance 的丢弃
        right = [0] + dfs(node.right)[:distance]
        right_prefix = list(accumulate(right))      # right_prefix[j]：距离 <= j 的右侧叶子数
        ans += sum(left[i] * right_prefix[distance - i] for i in range(distance + 1))
        return [a + b for a, b in zip(left, right)]

    dfs(root)
    return ans
```

运行：`[1,2,3,null,4]`、`3` → `1`，`[1,2,3,4,5,6,7]`、`3` → `2`，`[7,1,4,6,null,5,3,null,null,null,null,null,2]`、`3` → `1`，`[100]`、`1` → `0`，`[1,1,1]`、`2` → `1`；`1024` 个结点的单链 → `0`（调大递归上限后；默认上限下抛 `RecursionError`）；约 `1000` 个结点的满二叉树、`distance = 10` → `7936`，耗时不到 `1 ms`。

**复杂度。** 时间 `O(n · distance)`：每个节点常数个长度 `distance + 1` 的数组操作；空间 `O(h · distance)`：递归栈。

**写法要点。** `dfs` 返回数组、`nonlocal ans` 累计答案，一次后序遍历同时完成上报和统计；空节点返回全 `0` 数组，不需要判空；`[0] + c[:distance]` 一步完成“整体加一并截断到 `distance`”；`accumulate` 给出前缀和，让左右配对变成 `sum(left[i] * right_prefix[distance - i])`。
