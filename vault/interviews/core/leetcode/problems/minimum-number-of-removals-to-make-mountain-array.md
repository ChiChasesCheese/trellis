---
slug: minimum-number-of-removals-to-make-mountain-array
---
## Q
**LC 1671 得到山形数组的最少删除次数**｜Hard

山形数组：长度至少 3，存在峰顶下标 `i`（不在两端），使 `a[0] < … < a[i] > … > a[n-1]`。给数组 `nums`，求最少删除多少个元素能得到山形数组。

## A
**一句话。** 求最长山形子序列：对每个下标算「以它结尾的最长递增」和「以它开头的最长递减」，峰顶两侧都至少 2，答案是 `n - max(左 + 右 - 1)`。

```python
def minimum_mountain_removals(nums):
    n = len(nums)
    def lis_ending(a):                 # 以 a[i] 结尾的最长严格递增长度
        tails, res = [], []
        for x in a:
            k = bisect_left(tails, x)
            if k == len(tails):
                tails.append(x)
            else:
                tails[k] = x
            res.append(k + 1)
        return res
    pre = lis_ending(nums)
    suf = lis_ending(nums[::-1])[::-1]  # 以 nums[i] 开头的最长递减
    best = 0
    for i in range(1, n - 1):
        if pre[i] > 1 and suf[i] > 1:  # 两侧都要有元素
            best = max(best, pre[i] + suf[i] - 1)
    return n - best
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 不要求两侧都至少 2：只有上坡或只有下坡就不是山形，要排除 `pre[i] == 1` 或 `suf[i] == 1`。
- 峰顶重复计数：左右两段都含峰顶，长度相加后要减 1。
- 用 `bisect_right`：严格递增必须用 `bisect_left`，否则相等的值会被接上。

**追问。**
- 为什么能分开算两边？：峰顶固定后，左侧只依赖前缀，右侧只依赖后缀，互不影响。
- `O(n²)` 的版本？：`pre[i] = 1 + max(pre[j])`（`j < i`、`nums[j] < nums[i]`），数据小时更好写。

**同模式。** LC 300 最长递增子序列、LC 845 数组中的最长山脉、LC 941 有效的山脉数组、LC 334 递增的三元子序列
