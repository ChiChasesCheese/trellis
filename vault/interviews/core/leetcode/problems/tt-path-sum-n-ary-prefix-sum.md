---
slug: tt-path-sum-n-ary-prefix-sum
---
## Q
**N 叉树路径和（前缀和加哈希）**｜Medium

N 叉树（节点有 `val` 和 `children`，值可为负）和整数 `target`，统计自上而下（只往孩子方向、不必从根开始或到叶结束）的路径中和等于 `target` 的条数，要求 `O(n)`。

## A
**一句话。** DFS 维护根到当前节点的前缀和 `cur`，用 `Counter` 记路径上各前缀和的次数，答案加上 `seen[cur - target]`，离开节点时撤销（回溯）。

```python
def path_sum(root, target):
    seen = Counter({0: 1})    # 空前缀 0 出现 1 次

    def dfs(node, prefix):
        if node is None:
            return 0
        cur = prefix + node.val
        ans = seen[cur - target]    # 先查询
        seen[cur] += 1              # 再登记，供子孙配对
        for child in node.children:
            ans += dfs(child, cur)
        seen[cur] -= 1              # 回溯，兄弟看不到
        return ans

    return dfs(root, 0)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 忘了初始 `seen[0] = 1`：从根开始的路径漏掉，`Node(5)`、`target = 5` 得 `0`，应为 `1`。
- 先登记再查询：`Node(5)`、`target = 0` 把空路径数进去，得 `1`，应为 `0`。
- 不回溯：兄弟分支的前缀和残留在哈希表里，多数出路径。

**追问。**
- 二叉树版本？：就是 LC 437，把 `children` 换成 `left`、`right`。
- 链状树深度 `10^5`，递归超限？：调大 `setrecursionlimit`，或显式栈，栈里放一个「退出标记」弹出时撤销登记。

**同模式。** LC 437 路径总和 III、LC 560 和为 K 的子数组、LC 974 和可被 K 整除的子数组
