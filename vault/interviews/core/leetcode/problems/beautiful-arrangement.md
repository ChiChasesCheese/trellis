---
slug: beautiful-arrangement
---
## Q
**LC 526 优美的排列**｜Medium

把 `1..n` 排成数组，要求第 `i` 位的数 `p` 满足 `p % i == 0` 或 `i % p == 0`。求排列数量（`n <= 15`）。

## A
**一句话。** 回溯：按位置 1 到 `n` 依次填数，只选没用过且整除合法的数。

```python
def count_arrangement(n):
    used = [False] * (n + 1)

    def dfs(pos):
        if pos > n:
            return 1
        total = 0
        for num in range(1, n + 1):
            if used[num]:
                continue
            if num % pos == 0 or pos % num == 0:
                used[num] = True
                total += dfs(pos + 1)
                used[num] = False      # 撤销
        return total

    return dfs(1)
```

**复杂度。** 时间远小于 `O(n!)`（边填边剪枝），空间 `O(n)`。

**易错点。**
- 只检查一个方向的整除：`n=2` 的 `[2,1]` 要靠 `pos % num == 0`，会漏掉得 `1`。
- 忘了撤销 `used[num]`：后面分支看不到这个数，计数偏少。

**追问。**
- 为什么比生成全排列再过滤快？：`15!` 约 `1.3×10¹²`，边填边剪枝只剩约 `7.5×10⁵` 个节点。
- 还能怎么优化？：状压 DP，`dp[mask]` 以已用数字集合为状态，位置数就是 `popcount`。

**同模式。** LC 46 全排列、LC 51 N 皇后、LC 698 划分为 k 个相等的子集、LC 464 我能赢吗
