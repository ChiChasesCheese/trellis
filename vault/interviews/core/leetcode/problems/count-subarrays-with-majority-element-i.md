---
slug: count-subarrays-with-majority-element-i
---
## Q
**LC 3737 统计主要元素子数组数目 I**｜Medium

统计有多少子数组里 `target` 出现次数严格超过长度的一半。`n ≤ 1000`。

## A
**一句话。** `target` 记 `+1`、其他记 `-1`，子数组和 `> 0` 即过半；`n ≤ 1000`，枚举左端点、右端点边扩边累加。

```python
def count_majority_subarrays(nums, target):
    n, ans = len(nums), 0
    for i in range(n):
        bal = 0                  # target 个数 - 其他个数
        for j in range(i, n):
            bal += 1 if nums[j] == target else -1
            ans += bal > 0       # 严格过半
    return ans
```

**复杂度。** 时间 `O(n^2)`，空间 `O(1)`。

**易错点。**
- 写成 `bal >= 0`：恰好一半不算主要元素，`[2,1]` 会被误计。
- 每个子数组重新数一遍：`O(n^3)`。

**追问。**
- `n = 10^5`（LC 3739）？：前缀和 `s` 每步 `±1`，对每个 `j` 数前面有多少 `s[i] < s[j]`；用计数数组维护「比当前值小的个数」，每步只变一个值，`O(n)`。
- 为什么换成 `±1`？：「次数 > 长度一半」就是「target 个数 > 其他个数」，即区间和 `> 0`。

**同模式。** LC 525 连续数组、LC 560 和为 K 的子数组、LC 3739 统计主要元素子数组数目 II
