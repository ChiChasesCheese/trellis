---
slug: largest-divisible-subset
---
## Q
**LC 368 最大整除子集**｜Medium

互不相同的正整数集合，找最大子集使其中任意两数一个整除另一个，返回任一个。`n ≤ 1000`。

## A
**一句话。** 排序后整除有传递性，问题变成「整除版的最长递增子序列」：`f[i]` 是以 `nums[i]` 结尾的最长链，记前驱回溯出答案。

```python
def largest_divisible_subset(nums):
    nums.sort()
    n = len(nums)
    f = [1] * n                # 以 nums[i] 结尾的最长链
    pre = [-1] * n
    for i in range(n):
        for j in range(i):
            if nums[i] % nums[j] == 0 and f[j] + 1 > f[i]:
                f[i], pre[i] = f[j] + 1, j
    i = max(range(n), key=f.__getitem__)
    ans = []
    while i != -1:             # 沿前驱回溯
        ans.append(nums[i])
        i = pre[i]
    return ans[::-1]
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n)`。

**易错点。**
- 不排序：传递性只在有序时成立，`[4,8,2]` 会漏掉 `2|4|8`。
- 只求长度不记前驱：题目要返回子集本身。

**追问。**
- 为什么只需检查链尾？：`a | b | c` 且新数 `x` 被 `c` 整除，则 `x` 被链上每个数整除。
- 和 LIS 的区别？：转移条件从 `nums[j] < nums[i]` 换成 `nums[i] % nums[j] == 0`，不能用二分优化。

**同模式。** LC 300 最长递增子序列、LC 1048 最长字符串链、LC 673 最长递增子序列的个数
