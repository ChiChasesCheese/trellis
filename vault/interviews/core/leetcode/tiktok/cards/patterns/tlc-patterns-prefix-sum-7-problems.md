---
id: tlc-patterns-prefix-sum-7-problems
node: patterns.prefix-sum
type: qa
step: 7
---
## Q
**前缀和与差分（Prefix Sum）｜本组用到前缀和的题**

按变形分类，这个题组里哪些题用到前缀和或差分？

## A
**前缀和 + 哈希（子数组计数）**
- LC 560 和为 K 的子数组
- LC 974 和可被 K 整除的子数组（同余）
- LC 1248 统计「优美子数组」（奇偶映射成 0/1）
- LC 2845 统计趣味子数组的数目（高频）

**前缀和 + 二分 / 窗口**
- LC 209 长度最小的子数组（全正数，窗口或前缀和 + 二分）
- LC 528 按权重随机选择（前缀和 + `bisect`）

**差分 / 扫描线**
- LC 253 会议室 II（开始 +1、结束 -1 的差分思想）

**前缀统计 / 前缀最值**
- LC 1352 最后 K 个数的乘积（前缀积）
- LC 42 接雨水（前缀最大 / 后缀最大）

**TikTok 变体**
- 删除长度 k 的窗口使奇偶下标和相等（按原下标奇偶加符号的前缀和）

提示：每道题先写出 `pre` 的定义（前缀和、前缀乘积、前缀最大、奇数个数），再把条件翻译成 `pre[j] - pre[i]` 的关系。

**例题：** LC 560 和为 K 的子数组

整数数组 `nums` 和 `k`，统计和为 `k` 的连续非空子数组的个数。`1 <= nums.length <= 2 * 10^4`，`-1000 <= nums[i] <= 1000`，`-10^7 <= k <= 10^7`。

```python
from collections import Counter
def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})        # 前缀和 -> 出现次数；空前缀的和是 0
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - k]      # 以当前位置结尾、和为 k 的子数组个数
        seen[pre] += 1
    return ans
```

**例题：** LC 974 和可被 K 整除的子数组

整数数组 `nums` 和 `k`，统计和可被 `k` 整除的连续非空子数组的个数。`1 <= nums.length <= 3 * 10^4`，`-10^4 <= nums[i] <= 10^4`，`2 <= k <= 10^4`。

```python
from collections import Counter
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})                  # 前缀和模 k 的出现次数；空前缀的余数是 0
    prefix = ans = 0
    for x in nums:
        prefix = (prefix + x) % k           # Python 的 % 对负数也返回 [0, k)，不用再补 + k
        ans += seen[prefix]                 # 以当前位置结尾、余数相同的前缀每个对应一个合法子数组
        seen[prefix] += 1
    return ans
```

**例题：** LC 1248 统计「优美子数组」

整数数组 `nums` 和 `k`，统计恰好含 `k` 个奇数的连续子数组的个数。`1 <= nums.length <= 50000`，`1 <= nums[i] <= 10^5`，`1 <= k <= nums.length`。

```python
def number_of_subarrays(nums: list[int], k: int) -> int:
    seen = [0] * (len(nums) + 1)            # seen[j]：前缀里“恰好有 j 个奇数”的位置有多少个
    seen[0] = 1                             # 空前缀
    odd = ans = 0
    for x in nums:
        odd += x & 1                        # 前缀里奇数个数
        if odd >= k:
            ans += seen[odd - k]            # 左边前缀的奇数个数为 odd - k，中间恰好 k 个奇数
        seen[odd] += 1
    return ans
```

**例题：** LC 209 长度最小的子数组

正整数数组 `nums` 和 `target`，求和 `>= target` 的最短连续子数组的长度，没有返回 `0`。`1 <= nums.length <= 10^5`，`1 <= nums[i] <= 10^4`。

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

**例题：** LC 528 按权重随机选择

实现 `Solution(w)` 与 `pickIndex()`：返回下标 `i` 的概率是 `w[i] / sum(w)`。`1 <= w.length <= 10^4`，`1 <= w[i] <= 10^5`，最多调用 `10^4` 次。

```python
import random
from bisect import bisect_right
from itertools import accumulate
class Solution:
    def __init__(self, w: list[int]):
        self.prefix = list(accumulate(w))        # prefix[i] = w[0] + ... + w[i]
        self.total = self.prefix[-1]
    def pickIndex(self) -> int:
        r = random.randrange(self.total)         # 均匀落在 [0, total)
        return bisect_right(self.prefix, r)      # 第一个 prefix[i] > r 的 i
```

**例题：** LC 253 会议室 II

会议区间 `intervals`，求需要的最少会议室数（一个会议结束的时刻可以立刻开始下一个）。`1 <= intervals.length <= 10^4`，`0 <= start < end <= 10^6`。

```python
import heapq
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []                           # 小根堆：每个在用会议室的结束时间
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:              # 最早结束的会议已结束：复用它的房间
            heapq.heapreplace(ends, end)           # 弹出旧结束时间并压入新的，一次 O(log n)
        else:
            heapq.heappush(ends, end)              # 没有空房间：新开一间
    return len(ends)                               # 堆里剩几个 = 同时在用的房间数峰值
```

**例题：** LC 1352 最后 K 个数的乘积

实现 `ProductOfNumbers`：`add(num)` 在末尾追加一个数，`getProduct(k)` 返回最后 `k` 个数的乘积。`0 <= num <= 100`，`1 <= k <= 4 * 10^4`，任何连续段的乘积都在 32 位整数内，总共最多 `4 * 10^4` 次调用。

```python
class ProductOfNumbers:
    def __init__(self) -> None:
        self.prefix: list[int] = [1]        # prefix[i]：最近一个 0 之后前 i 个数的乘积，prefix[0] = 1
    def add(self, num: int) -> None:
        if num == 0:
            self.prefix = [1]               # 遇到 0：之前的前缀全部作废，重新开始
        else:
            self.prefix.append(self.prefix[-1] * num)
    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):           # 最后 k 个数跨过了最近的 0
            return 0
        return self.prefix[-1] // self.prefix[-1 - k]   # 前缀积相除，整除是精确的
```

**例题：** LC 42 接雨水

非负整数数组 `height` 表示宽度为 `1` 的柱子的高度，求下雨后能接多少雨水。`1 <= n <= 2 * 10^4`，`0 <= height[i] <= 10^5`。

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:           # 左边更矮：左格的水位由 left_max 决定
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:                                      # 右边更矮或相等：右格的水位由 right_max 决定
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

**例题：** LC 2845 统计趣味子数组的数目

给下标从 `0` 开始的整数数组 `nums`，以及整数 `modulo` 和 `k`。如果子数组 `nums[l..r]` 满足：设 `cnt` 为区间 `[l, r]` 内满足 `nums[i] % modulo == k` 的下标 `i` 的个数，并且 `cnt % modulo == k`，就称它为**趣味子数组**。返回趣味子数组的数目。`1 <= nums.length <= 10^5`，`1 <= nums[i] <= 10^9`，`1 <= modulo <= 10^9`，`0 <= k < modulo`。

```python
from collections import Counter


def count_interesting_subarrays(nums: list[int], modulo: int, k: int) -> int:
    seen: Counter[int] = Counter({0: 1})           # 前缀计数（对 modulo 取模）出现的次数，空前缀算一次
    pre = ans = 0
    for x in nums:
        pre = (pre + (x % modulo == k)) % modulo   # 到当前位置，满足条件的元素个数 mod modulo
        ans += seen[(pre - k) % modulo]            # 需要某个旧前缀 p 使得 (pre - p) % modulo == k
        seen[pre] += 1
    return ans
```

**例题：** 删除长度 k 的窗口使奇偶下标和相等

删除数组 `nums` 里一段长度恰为 `k` 的连续子数组，剩余元素重新编号后要求偶数下标之和等于奇数下标之和，返回最小的删除起点，没有返回 `-1`；`n <= 10^5`。

```python
from itertools import accumulate
def min_balanced_deletion(nums: list[int], k: int) -> int:
    """删除一段长度 k 的连续子数组，使剩余数组偶数下标之和等于奇数下标之和；返回最小起点，没有则返回 -1。"""
    n = len(nums)
    pre = list(accumulate((x if i % 2 == 0 else -x for i, x in enumerate(nums)), initial=0))
    flip = -1 if k % 2 else 1
    for i in range(n - k + 1):
        left = pre[i]
        right = flip * (pre[n] - pre[i + k])
        if left + right == 0:
            return i
    return -1
```
