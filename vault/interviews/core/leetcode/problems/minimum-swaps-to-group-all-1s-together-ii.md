---
slug: minimum-swaps-to-group-all-1s-together-ii
---
## Q
**LC 2134 最少交换次数来组合所有的 1 II**｜Medium

二进制环形数组 `nums`（首尾相邻），求把所有 `1` 聚到一起所需的最少交换次数（交换任意两个位置）。

## A
**一句话。** 设 `1` 的个数为 `k`，在环上滑动长为 `k` 的窗口，答案是 `k` 减去窗口里最多的 `1`。

```python
def min_swaps(nums):
    n, ones = len(nums), sum(nums)
    window = sum(nums[:ones])       # 起点 0 的窗口里的 1
    best = window
    for i in range(ones, ones + n - 1):   # 下标取模当作环
        window += nums[i % n] - nums[(i - ones) % n]
        best = max(best, window)
    return ones - best      # 窗口里的 0 = 要换进来的 1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只枚举线性窗口：`[1,1,0,0,1]` 得 `1`，环形下应为 `0`，跨越末尾的窗口漏了。
- 返回 `best` 而不是 `ones - best`：`[0,1,0,1,1,0,0]` 得 `2`，应为 `1`。
- 右端忘了取模：`i >= n` 时 `nums[i]` 越界。

**追问。**
- 非环形（LC 1151）怎么改？：去掉取模，窗口起点只取 `0..n-k`。
- 有更好读的写法吗？：`nums + nums` 的前缀和，答案 `ones - max(pref[i+ones] - pref[i])`，空间 `O(n)`。

**同模式。** LC 1151 最少交换次数来组合所有的 1、LC 1004 最大连续 1 的个数 III、LC 918 环形子数组的最大和、LC 1658 将 x 减到 0 的最小操作数
