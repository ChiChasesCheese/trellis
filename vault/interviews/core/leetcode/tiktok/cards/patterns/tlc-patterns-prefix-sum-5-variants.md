---
id: tlc-patterns-prefix-sum-5-variants
node: patterns.prefix-sum
type: qa
step: 5
---
## Q
**前缀和与差分（Prefix Sum）｜变形：二维前缀和、扫描线、前缀最值、值域差分**

二维前缀和怎么算？会议室这类覆盖计数怎么用差分？最大子数组和（LC 53）和接雨水（LC 42）里前缀和、前缀最值起什么作用？

## A
**二维前缀和**：`p[r+1][c+1]` = 左上角到 `(r, c)` 的矩形和，容斥原理（高频：LC 560 和为 K 的子数组）。

```python
class NumMatrix:
    def __init__(self, m: list[list[int]]) -> None:
        R, C = len(m), len(m[0])
        self.p = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.p[r+1][c+1] = m[r][c] + self.p[r][c+1] + self.p[r+1][c] - self.p[r][c]
    def region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        p = self.p
        return p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1] + p[r1][c1]
```

**LC 253 会议室 II**：时间点很多，用字典做稀疏差分，开始 `+1`、结束 `-1`，排序后扫描，扫描时的最大累计值就是同时进行的会议数（例：LC 253 会议室 II）：

```python
from collections import Counter
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    diff: Counter[int] = Counter()
    for start, end in intervals:
        diff[start] += 1
        diff[end] -= 1                # 半开区间 [start, end)：结束那一刻房间已经空出来
    best = cur = 0
    for t in sorted(diff):
        cur += diff[t]
        best = max(best, cur)
    return best
print(min_meeting_rooms([[0, 30], [5, 10], [15, 20]]), min_meeting_rooms([[7, 10], [2, 4]]), min_meeting_rooms([[1, 5], [5, 9]]))   # 2 1 1
```

- **LC 53**：子数组和 = `pre[j] - pre[i]`，固定右端 `j`，要最大就取 `i < j` 里最小的前缀和，用一个变量 `min_pre` 边扫边维护（例：LC 53 最大子数组和）。
- **LC 42**：每根柱子上方的水位 = `min(左侧最高, 右侧最高)`，两个方向的前缀最大值各用一次 `accumulate(…, max)` 得到（例：LC 42 接雨水）。
- **LC 209**：元素全为正 → 前缀和严格递增 → `bisect_left(pre, pre[i] + target)` 找右端，`O(n log n)`（例：LC 209 长度最小的子数组）。

**例题：** LC 253 会议室 II

给一个会议时间数组 `intervals`，`intervals[i] = [starti, endi]`，返回所需会议室的最小数量。`1 <= intervals.length <= 10^4`，`0 <= starti < endi <= 10^6`。

```python
from collections import Counter
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    diff: Counter[int] = Counter()               # 差分：在时刻 t，同时进行的会议数变化多少
    for start, end in intervals:
        diff[start] += 1                         # 会议开始：需要多一个房间
        diff[end] -= 1                           # 会议结束：释放一个房间
    best = cur = 0
    for t in sorted(diff):                       # 只有事件时刻才会变化，按时间从小到大扫
        cur += diff[t]
        best = max(best, cur)                    # 同一时刻的结束与开始先合并成净变化，首尾相接的会议不会多占房间
    return best
```

**例题：** LC 53 最大子数组和

整数数组 `nums`（`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`），求和最大的连续子数组（至少一个元素）的和。

```python
def max_sub_array(nums: list[int]) -> int:
    best = nums[0]
    pre = min_pre = 0                      # pre：当前前缀和；min_pre：此前出现过的最小前缀和（含空前缀 0）
    for x in nums:
        pre += x
        best = max(best, pre - min_pre)    # 以当前位置结尾的最大子数组和 = 前缀和 - 之前最小前缀和
        min_pre = min(min_pre, pre)        # 先用后更新：保证子数组非空
    return best
```

**例题：** LC 42 接雨水

`n` 个非负整数表示宽度为 1 的柱子的高度图（`1 <= n <= 2 * 10^4`，`0 <= height[i] <= 10^5`），计算下雨之后能接多少雨水。

```python
from itertools import accumulate

def trap(height: list[int]) -> int:
    left_max = list(accumulate(height, max))                      # left_max[i]：height[0..i] 的最大值
    right_max = list(accumulate(reversed(height), max))[::-1]     # right_max[i]：height[i..] 的最大值
    return sum(min(l, r) - h for h, l, r in zip(height, left_max, right_max))   # 水位 = 两侧最高中较矮的一侧，减去柱高
```

**例题：** LC 209 长度最小的子数组

正整数数组 `nums`（`1 <= length <= 10^5`，`1 <= v <= 10^4`）和 `target`（`1 <= target <= 10^9`），求和大于等于 `target` 的最短连续子数组长度，没有则为 `0`。

```python
def min_sub_array_len(target: int, nums: list[int]) -> int:
    best = len(nums) + 1                    # 哨兵：比任何合法长度都大
    left = total = 0
    for right, x in enumerate(nums):
        total += x                          # 右端吃进 x
        while total >= target:              # 窗口和够了：尽量缩左端，每缩一步都是一个候选答案
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
```

**例题：** LC 560 和为 K 的子数组

给整数数组 `nums` 和整数 `k`，统计并返回该数组中**和为 `k` 的子数组的个数**。子数组是数组中元素的连续非空序列。`1 <= nums.length <= 2 * 10^4`，`-1000 <= nums[i] <= 1000`，`-10^7 <= k <= 10^7`。

```python
from collections import Counter
def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - k]
        seen[pre] += 1
    return ans
```
