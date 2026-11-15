---
slug: house-robber-iv
---
## Q
**LC 2560 打家劫舍 IV**｜Medium

一排房屋金额 `nums`，不能偷相邻的两间，至少偷 `k` 间。窃取能力 = 偷过的单间最大金额，求最小窃取能力。

## A
**一句话。** 最小化最大值，二分能力 `c`：只偷金额 `<= c` 的房子，从左往右能偷就偷（贪心），数够 `k` 间即可行。

```python
def min_capability(nums, k):
    def enough(c):              # 只偷 <= c 的，能偷够 k 间吗
        cnt = i = 0
        while i < len(nums):
            if nums[i] <= c:
                cnt += 1
                i += 2          # 偷了就跳过邻居
            else:
                i += 1
        return cnt >= k

    lo, hi = min(nums), max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log U)`，空间 `O(1)`。

**易错点。**
- 用打家劫舍的金额和 DP 去判定：要的是间数，不是金额。
- 判定里偷了一间只 `i += 1`：会连偷相邻的两间，可行性被高估。

**追问。**
- 为什么能偷就偷是对的？：偷第 `i` 间最多挡住 `i+1`，若不偷 `i` 而偷 `i+1` 只会更晚，交换论证可知不亏。
- 只在 `nums` 的值上二分？：先排序去重，在下标上二分，次数降到 `log n`。

**同模式。** LC 198 打家劫舍、LC 875 爱吃香蕉的珂珂、LC 410 分割数组的最大值、LC 2616 最小化数对的最大差值
