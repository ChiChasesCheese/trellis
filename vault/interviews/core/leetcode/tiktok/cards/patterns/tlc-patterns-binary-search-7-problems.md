---
id: tlc-patterns-binary-search-7-problems
node: patterns.binary-search
type: qa
step: 7
---
## Q
**二分查找（Binary Search）｜本组用到二分的题**

按变形分类，这个题组里哪些题用二分？

## A
**有序数组上的边界**
- LC 34 在排序数组中查找元素的第一个和最后一个位置
- LC 69 x 的平方根
- LC 35 搜索插入位置（高频）
- LC 2300 咒语和药水的成功对数（高频）

**旋转 / 峰值 / 成对结构**
- LC 33 搜索旋转排序数组
- LC 153 寻找旋转排序数组中的最小值
- LC 162 寻找峰值
- LC 540 有序数组中的单一元素
- LC 154 寻找旋转排序数组中的最小值 II（高频）
- LC 4 寻找两个正序数组的中位数（高频）

**对答案二分（最小化最大值）**
- LC 875 爱吃香蕉的珂珂
- LC 1011 在 D 天内送达包裹的能力
- LC 378 有序矩阵中第 K 小的元素（值域二分）
- LC 1918 第 K 小的子数组和（高频）

**二分 + 前缀和 / 其他结构**
- LC 209 长度最小的子数组（前缀和 + 二分）
- LC 528 按权重随机选择（前缀和 + `bisect`）
- LC 300 最长递增子序列（`tails` 数组上二分）
- LC 981 基于时间的键值存储（高频）

提示：先看是在**下标**上二分还是对**答案**二分；再写判定函数，确认它是 `False...False True...True`；最后选模板。

**例题：** LC 34 在排序数组中查找元素的第一个和最后一个位置

非递减整数数组 `nums` 和 `target`，返回 `target` 的起止下标，不存在返回 `[-1, -1]`，要求 `O(log n)`；`0 <= nums.length <= 10^5`。

```python
from bisect import bisect_left, bisect_right
def search_range(nums: list[int], target: int) -> list[int]:
    lo = bisect_left(nums, target)
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]
    hi = bisect_right(nums, target) - 1
    return [lo, hi]
```

**例题：** LC 69 x 的平方根

给非负整数 `x`，返回 `floor(sqrt(x))`，不许用 `pow` 或 `**0.5`；`0 <= x <= 2^31 - 1`。

```python
def my_sqrt(x: int) -> int:
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**例题：** LC 33 搜索旋转排序数组

元素互不相同的升序数组在某处旋转后得到 `nums`，在 `O(log n)` 内返回 `target` 的下标，不存在返回 `-1`；`1 <= nums.length <= 5000`。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**例题：** LC 153 寻找旋转排序数组中的最小值

元素互不相同的升序数组旋转后得到 `nums`，在 `O(log n)` 内返回最小元素；`1 <= n <= 5000`。

```python
def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
```

**例题：** LC 162 寻找峰值

峰值是严格大于左右邻居的元素（两端之外视为 `-∞`），相邻元素不相等；返回任意一个峰值的下标，要求 `O(log n)`；`1 <= nums.length <= 1000`。

```python
def find_peak_element(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

**例题：** LC 540 有序数组中的单一元素

有序数组里每个数出现两次，只有一个数出现一次，找出它，要求 `O(log n)` 时间、`O(1)` 空间；`1 <= nums.length <= 10^5`。

```python
def single_non_duplicate(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        mid -= mid & 1
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return nums[lo]
```

**例题：** LC 875 爱吃香蕉的珂珂

`piles[i]` 堆香蕉，每小时选一堆吃最多 `k` 根，求 `h` 小时内吃完的最小速度 `k`；`piles.length <= h <= 10^9`，`piles[i] <= 10^9`。

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum((p + mid - 1) // mid for p in piles)
        if hours <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**例题：** LC 1011 在 D 天内送达包裹的能力

包裹按顺序装船，每天装的总重不超过载重，求 `days` 天内送完的最低载重；`1 <= days <= weights.length <= 5 * 10^4`，`weights[i] <= 500`。

```python
def ship_within_days(weights: list[int], days: int) -> int:
    def days_needed(capacity: int) -> int:
        used, load = 1, 0
        for w in weights:
            if load + w > capacity:
                used += 1
                load = 0
            load += w
        return used
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**例题：** LC 378 有序矩阵中第 K 小的元素

`n x n` 矩阵每行每列都非递减，求排序后的第 `k` 小元素（重复值各算一个），内存优于 `O(n^2)`；`n <= 300`。

```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)
    def count_le(mid: int) -> int:
        count, col = 0, n - 1
        for row in matrix:
            while col >= 0 and row[col] > mid:
                col -= 1
            count += col + 1
        return count
    lo, hi = matrix[0][0], matrix[-1][-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**例题：** LC 209 长度最小的子数组

正整数数组 `nums` 和 `target`，求和不小于 `target` 的最短连续子数组的长度，没有返回 `0`；`nums.length <= 10^5`。

```python
def min_sub_array_len(target: int, nums: list[int]) -> int:
    best = len(nums) + 1
    left = total = 0
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
```

**例题：** LC 528 按权重随机选择

实现 `pickIndex()`，返回下标 `i` 的概率为 `w[i] / sum(w)`；`w.length <= 10^4`，`w[i] <= 10^5`，最多调用 `10^4` 次。

```python
import random
from bisect import bisect_right
from itertools import accumulate
class Solution:
    def __init__(self, w: list[int]):
        self.prefix = list(accumulate(w))
        self.total = self.prefix[-1]
    def pickIndex(self) -> int:
        r = random.randrange(self.total)
        return bisect_right(self.prefix, r)
```

**例题：** LC 300 最长递增子序列

整数数组 `nums`，求最长严格递增子序列的长度（不要求连续）；`nums.length <= 2500`，进阶 `O(n log n)`。

```python
from bisect import bisect_left
def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

**例题：** LC 35 搜索插入位置

升序、无重复元素的整数数组 `nums` 和目标值 `target`：找到就返回下标，找不到就返回它按顺序插入后应在的下标，要求 `O(log n)`；`1 <= nums.length <= 10^4`。

```python
def search_insert(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

**例题：** LC 2300 咒语和药水的成功对数

给咒语数组 `spells` 和药水数组 `potions`，两者能量相乘 `>= success` 就是一对成功的组合；返回每个咒语能成功配对的药水数量；`1 <= n, m <= 10^5`，`1 <= spells[i], potions[j] <= 10^5`，`1 <= success <= 10^10`。

```python
from bisect import bisect_left
def successful_pairs(spells: list[int], potions: list[int], success: int) -> list[int]:
    potions = sorted(potions)
    m = len(potions)
    return [m - bisect_left(potions, success, key=lambda p: p * s) for s in spells]
```

**例题：** LC 154 寻找旋转排序数组中的最小值 II

升序数组旋转后得到 `nums`，**允许重复元素**，返回最小元素；`1 <= nums.length <= 5000`。

```python
def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        elif nums[mid] < nums[hi]:
            hi = mid
        else:
            hi -= 1
    return nums[lo]
```

**例题：** LC 4 寻找两个正序数组的中位数

两个升序数组 `nums1`、`nums2`，返回合并后的中位数，时间复杂度要求 `O(log(m + n))`；`0 <= m, n <= 1000`，`1 <= m + n <= 2000`。

```python
from math import inf
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    a, b = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        a_left = a[i - 1] if i > 0 else -inf
        a_right = a[i] if i < m else inf
        b_left = b[j - 1] if j > 0 else -inf
        b_right = b[j] if j < n else inf
        if a_left > b_right:
            hi = i - 1
        elif b_left > a_right:
            lo = i + 1
        else:
            left_max = max(a_left, b_left)
            if (m + n) % 2:
                return float(left_max)
            return (left_max + min(a_right, b_right)) / 2
    raise ValueError("输入不是有序数组")
```

**例题：** LC 1918 第 K 小的子数组和

正整数数组 `nums`，返回第 `k` 小的子数组和（子数组是非空连续段，位置不同的子数组各算一个）；`1 <= nums.length <= 2 * 10^4`，`1 <= nums[i] <= 5 * 10^4`。

```python
def kth_smallest_subarray_sum(nums: list[int], k: int) -> int:
    def count_le(x: int) -> int:
        cnt = left = cur = 0
        for right, v in enumerate(nums):
            cur += v
            while cur > x:
                cur -= nums[left]
                left += 1
            cnt += right - left + 1
        return cnt
    lo, hi = min(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**例题：** LC 981 基于时间的键值存储

实现 `TimeMap`：`set(key, value, timestamp)` 存值，`get(key, timestamp)` 返回时间戳不超过 `timestamp` 的最近一次 `set` 的值，没有则返回 `""`；同一个键的 `set` 时间戳严格递增，调用总数 `<= 2 * 10^5`。

```python
from bisect import bisect_right
from collections import defaultdict
class TimeMap:
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)
        self.values: defaultdict[str, list[str]] = defaultdict(list)
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)
        self.values[key].append(value)
    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)
        if not times:
            return ""
        i = bisect_right(times, timestamp)
        return self.values[key][i - 1] if i else ""
```
