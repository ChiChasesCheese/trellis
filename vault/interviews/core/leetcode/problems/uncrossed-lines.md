---
slug: uncrossed-lines
---
## Q
**LC 1035 不相交的线**｜Medium

把 `nums1`、`nums2` 分两行写下，相等的数之间可以连线，且线不能相交、每个数至多连一条线。求最多能连多少条线。

## A
**一句话。** 线不相交意味着连线的数对保持相对顺序，就是求两个数组的最长公共子序列（LCS）。

```python
def max_uncrossed_lines(nums1, nums2):
    m, n = len(nums1), len(nums2)
    # f[i][j]：nums1 前 i 个、nums2 前 j 个的最多连线
    f = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if nums1[i] == nums2[j]:
                f[i + 1][j + 1] = f[i][j] + 1     # 连这一对
            else:
                f[i + 1][j + 1] = max(f[i][j + 1],
                                      f[i + 1][j])
    return f[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 把「线不相交」当成难点：连线的两个下标一个增则另一个也增，正是子序列保持顺序，直接套 LCS 模板。
- 相等时还去取 `max`：相等就连，`f[i][j] + 1` 一定不比跳过差。

**追问。**
- 为什么相等时直接连不会错？：LCS 的标准性质，匹配末尾字符总在某个最优解里。
- 和 LC 1143 的区别？：只是数组代替字符串，代码完全一样。

**同模式。** LC 1143 最长公共子序列、LC 583 两个字符串的删除操作、LC 712 两个字符串的最小ASCII删除和
