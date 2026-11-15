---
slug: maximum-compatibility-score-sum
---
## Q
**LC 1947 最大兼容性评分和**｜Medium

`m` 名学生和 `m` 名导师各自回答 `n` 道是非题（`0/1`）。把每名学生与恰好一位导师配对，兼容性评分是两人答案相同的题数。求所有配对的评分之和的最大值（`m <= 8`）。

## A
**一句话。** 状压 DP：按学生顺序依次配导师，`dp[mask]` 表示已被配走的导师集合为 `mask` 时的最大评分，已配学生数就是 `mask` 的位数。

```python
def max_compatibility_sum(students, mentors):
    m = len(students)
    score = [[sum(a == b for a, b in zip(s, t))
              for t in mentors] for s in students]
    dp = [-1] * (1 << m)
    dp[0] = 0
    for mask in range(1 << m):
        if dp[mask] < 0:
            continue
        i = bin(mask).count('1')          # 下一个要配的学生
        if i == m:
            continue
        for j in range(m):
            if not mask >> j & 1:
                nm = mask | 1 << j
                dp[nm] = max(dp[nm], dp[mask] + score[i][j])
    return dp[(1 << m) - 1]
```

**复杂度。** 时间 `O(2^m · m)`，空间 `O(2^m)`。

**易错点。**
- 枚举全排列：`8! = 40320` 能过，但 `m` 再大就不行，状压是通用解。
- 学生序号用循环变量：状压里学生是由 `mask` 的位数推出的。

**追问。**
- 更大规模怎么办？：这是二分图最大权匹配，用匈牙利算法 `O(m³)`。

**同模式。** LC 1066 校园自行车分配 II、LC 2172 数组的最大与和、LC 1879 两个数组最小的异或值之和、LC 526 优美的排列
