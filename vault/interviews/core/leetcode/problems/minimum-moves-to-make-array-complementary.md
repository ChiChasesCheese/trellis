---
slug: minimum-moves-to-make-array-complementary
---
## Q
**LC 1674 使数组互补的最少操作次数**｜Medium

偶数长度数组，每次可把一个数改成 `1..limit` 里的任意数。求使所有 `nums[i] + nums[n-1-i]` 相等的最少操作数。

## A
**一句话。** 对每一对，让和等于 `s` 的代价是 `0/1/2` 的分段常数，用差分数组累加所有对，前缀和后在 `s ∈ [2, 2*limit]` 上取最小。

```python
def min_moves(nums, limit):
    n = len(nums)
    diff = [0] * (2 * limit + 2)
    for a, b in zip(nums[:n//2], reversed(nums[n//2:])):
        lo, hi = min(a, b), max(a, b)
        diff[2] += 2               # 默认改两个
        diff[lo + 1] -= 1          # [lo+1, hi+limit]：改一个
        diff[hi + limit + 1] += 1
        diff[a + b] -= 1           # s == a+b：不用改
        diff[a + b + 1] += 1
    cost = list(accumulate(diff))
    return min(cost[2:2 * limit + 1])
```

**复杂度。** 时间 `O(n + limit)`，空间 `O(limit)`。

**易错点。**
- 区间左端写成 `lo`：改一个数后新和最小是 `lo + 1`，`[1,2,2,1]`、`limit = 2` 得 `1`，应为 `2`。
- 只试已有的 `a + b` 当目标和：`[4,3,2,1,1,1,4,4]`、`limit = 4` 得 `5`，应为 `4`。
- 差分数组开小：下标最大到 `2*limit + 1`，长度至少 `2*limit + 2`。

**追问。**
- `limit` 极大而 `n` 很小怎么办？：改成稀疏事件点排序扫描，`O(n log n)`。
- 如何返回最优的目标和？：扫前缀和时记录取最小值的 `s`。

**同模式。** LC 1109 航班预订统计、LC 370 区间加法、LC 1094 拼车、LC 253 会议室 II
