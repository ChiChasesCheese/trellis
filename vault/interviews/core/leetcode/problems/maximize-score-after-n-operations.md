---
slug: maximize-score-after-n-operations
---
## Q
**LC 1799 N 次操作后的最大分数和**｜Hard

长度 `2n`（`n <= 7`）的正整数数组，做 `n` 次操作：第 `i` 次选两个数 `x, y` 删掉，得分 `i · gcd(x, y)`。求总分最大值。

## A
**一句话。** 状压 DP：`mask` 记已删掉的数，操作序号由 `mask` 中 1 的个数决定；每次固定最低的未删元素，枚举它的搭档。

```python
def max_score(nums):
    m = len(nums)
    g = [[gcd(a, b) for b in nums] for a in nums]

    @cache
    def dfs(mask):               # mask：已删掉的元素
        if mask == (1 << m) - 1:
            return 0
        op = mask.bit_count() // 2 + 1   # 第几次操作
        i = (~mask & (mask + 1)).bit_length() - 1
        best = 0                 # i：最低的未删元素
        for j in range(i + 1, m):
            if not mask >> j & 1:
                nxt = mask | 1 << i | 1 << j
                best = max(best, op * g[i][j] + dfs(nxt))
        return best

    return dfs(0)
```

**复杂度。** 时间 `O(2^{2n}·n)`，空间 `O(2^{2n})`。

**易错点。**
- 枚举所有 `(i, j)` 对：同一组配对会按不同顺序重复算，固定最低未删元素可去掉 `n` 倍的重复。
- 操作序号另开参数传：会让状态数翻倍，序号可以由 `mask` 推出。

**追问。**
- 为什么固定最低位不丢解？：它迟早要被删，只是和谁配对的问题，枚举搭档就覆盖了所有配对。
- 能贪心把最大的 gcd 放最后吗？：配对之后可以按 gcd 排序分配序号，但选哪些配对仍需搜索。

**同模式。** LC 78 子集、LC 698 划分为k个相等的子集、LC 1879 两个数组最小的异或值之和
