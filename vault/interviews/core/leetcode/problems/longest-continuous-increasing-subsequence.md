---
slug: longest-continuous-increasing-subsequence
---
## Q
**LC 674 最长连续递增序列**｜Easy

给未排序的整数数组，返回最长的连续、严格递增子序列（即子数组）的长度。

## A
**一句话。** 一趟扫描：比前一个大就把当前递增段长度加一，否则重置为 1，答案取最大值。

```python
def find_length_of_lcis(nums):
    ans = run = 1                    # 单个元素长度为 1
    for i in range(1, len(nums)):
        run = run + 1 if nums[i] > nums[i - 1] else 1
        ans = max(ans, run)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 把「相等」也当递增：题目要严格递增，写成 `>`，不是 `>=`。
- 与 LIS 混淆：这里要连续，断了就重置，不需要 `O(n²)` 的 DP。
- 空数组：约束保证至少 1 个元素；若可能为空要先返回 `0`。

**追问。**
- 和最长递增子序列（LC 300）差在哪？：子序列可以跳着取，要 DP 或二分；子数组只看相邻，扫一遍。
- 要返回这一段本身？：记下最长段的起点，`nums[start:start+ans]`。

**同模式。** LC 300 最长递增子序列、LC 128 最长连续序列、LC 376 摆动序列、LC 978 最长湍流子数组
