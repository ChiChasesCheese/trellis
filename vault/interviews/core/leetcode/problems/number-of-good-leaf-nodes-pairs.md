---
slug: number-of-good-leaf-nodes-pairs
---
## Q
**LC 1530 好叶子节点对的数量**｜Medium

二叉树中两叶子的最短路径长 `<= distance` 即为好叶子对，数一共有多少对。

## A
**一句话。** 树形 DP：每个节点上报 `cnt[d]`（子树里距它恰好 `d` 的叶子数），在 LCA 处用左右数组配对。

```python
def count_pairs(root, distance):
    ans = 0
    def dfs(node):               # 返回 cnt[0..distance]
        nonlocal ans
        if not node:
            return [0] * (distance + 1)
        if not node.left and not node.right:
            return [1] + [0] * distance
        left = [0] + dfs(node.left)[:distance]    # 向上多 1 步
        right = [0] + dfs(node.right)[:distance]
        pre = list(accumulate(right))     # 距离 <= j 的右侧叶子数
        ans += sum(left[i] * pre[distance - i]
                   for i in range(distance + 1))
        return [a + b for a, b in zip(left, right)]
    dfs(root)
    return ans
```

**复杂度。** 时间 `O(n·distance)`，空间 `O(h·distance)`。

**易错点。**
- 条件写成 `<`：`[1,2,3,null,4]`、`distance=3` 得 `0`，应为 `1`。
- 同侧也配对：叶子对只在 LCA 处按「左 x 右」数一次。
- 链状树深 1023 超过 CPython 默认递归上限，要调大 `setrecursionlimit`。

**追问。**
- 要返回具体的叶子对？：数组里存叶子本身而不是个数。
- `distance` 很大怎么办？：数组合并变成 `O(n^2)`，改用长链剖分或点分治。

**同模式。** LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 687 最长同值路径、LC 834 树中距离之和
