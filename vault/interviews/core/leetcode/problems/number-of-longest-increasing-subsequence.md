---
slug: number-of-longest-increasing-subsequence
---
## Q
**LC 673 最长递增子序列的个数**｜Medium

返回数组 `nums` 中最长严格递增子序列的个数。

## A
**一句话。** 在 LIS 的 `O(n^2)` DP 上多带 `count`：找到更长的就覆盖计数，一样长就累加。

```python
def find_number_of_lis(nums):
    n = len(nums)
    length = [1] * n     # 以 nums[i] 结尾的最长长度
    count = [1] * n      # 达到该长度的个数
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
    best = max(length)
    return sum(c for l, c in zip(length, count)
               if l == best)
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n)`。

**易错点。**
- 更长时写成 `count[i] += count[j]`：带上了旧计数，`[1,3,5,4,7]` 得 `12`，应为 `2`。
- 返回 `count[-1]` 或第一个最长位置的计数：`[2,2,2,2,2]` 得 `1`，应为 `5`。
- 把 `<` 写成 `<=`：相等元素也被串起来，`[2,2,2,2,2]` 得 `1`。

**追问。**
- 只求长度（LC 300）？：`tails` 数组加 `bisect_left`，`O(n log n)`。
- 个数也做到 `O(n log n)`？：按长度分层，每层按结尾值维护方案数前缀和并二分，或用树状数组。

**同模式。** LC 300 最长递增子序列、LC 646 最长数对链、LC 354 俄罗斯套娃信封问题、LC 376 摆动序列
