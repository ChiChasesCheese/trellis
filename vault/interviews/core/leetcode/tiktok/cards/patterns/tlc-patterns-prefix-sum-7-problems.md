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

**前缀和 + 二分 / 窗口**
- LC 209 长度最小的子数组（全正数，窗口或前缀和 + 二分）
- LC 528 按权重随机选择（前缀和 + `bisect`）
- LC 1151 最少交换次数来组合所有的 1（固定窗口里 1 的个数，前缀和或窗口计数）
- LC 3086 拾起 K 个 1 需要的最少行动次数（前缀和 + 窗口）

**差分 / 扫描线**
- LC 2021 街上最亮的位置
- LC 253 会议室 II（开始 +1、结束 -1 的差分思想）

**前缀统计 / 前缀最值**
- LC 2640 一个数组所有前缀的分数
- LC 2145 统计隐藏数组数目
- LC 1352 最后 K 个数的乘积（前缀积）
- LC 42 接雨水（前缀最大 / 后缀最大）

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

**例题：** LC 1151 最少交换次数来组合所有的 1

二进制数组 `data`，每次可以交换任意两个位置，求把所有 `1` 聚到一起的最少交换次数。`1 <= data.length <= 10^5`。

```python
def min_swaps(data: list[int]) -> int:
    w = sum(data)                         # 窗口宽度 = 1 的总数
    cur = sum(data[:w])                   # 第一个窗口里已有的 1
    best = cur
    for i in range(w, len(data)):
        cur += data[i] - data[i - w]      # 右端进一个、左端出一个
        best = max(best, cur)
    return w - best                       # 窗口里的 0 的个数 = 需要换进来的 1 的个数
```

**例题：** LC 3086 拾起 K 个 1 需要的最少行动次数

二进制数组 `nums`、`k`、`maxChanges`。Alice 选一个站位（该位是 `1` 就免费拾起），之后每次行动要么把某个 `0` 改成 `1`（最多 `maxChanges` 次），要么交换相邻的 `1` 和 `0`（`1` 移到她脚下时拾起）。求恰好拾起 `k` 个 `1` 的最少行动次数。`2 <= n <= 10^5`，`maxChanges + sum(nums) >= k`。

```python
from itertools import accumulate, groupby
def minimum_moves(nums: list[int], k: int, max_changes: int) -> int:
    # c：Alice 站在某个 1 上，不用"造 1"就能拿到的相邻 1 的个数（0、1、1 步），最多 3 个
    longest_run = max((len(list(g)) for v, g in groupby(nums) if v), default=0)
    c = min(longest_run, 3, k)
    if max_changes >= k - c:                   # 剩下的 k-c 个全靠"造 1 再换过来"，每个 2 步
        return max(c - 1, 0) + 2 * (k - c)
    # 否则造 1 的次数全部用完，还得把 need 个已有的 1 挪到 Alice 身边
    need = k - max_changes
    pos = [i for i, x in enumerate(nums) if x]
    pre = list(accumulate(pos, initial=0))     # pre[i] = pos[0] + ... + pos[i-1]
    def cost(l: int) -> int:                   # 窗口 pos[l : l+need] 全部挪向中位数的总步数
        r, m = l + need, l + need // 2
        left = pos[m] * (m - l) - (pre[m] - pre[l])
        right = (pre[r] - pre[m + 1]) - pos[m] * (r - m - 1)
        return left + right
    return 2 * max_changes + min(map(cost, range(len(pos) - need + 1)))
```

**例题：** LC 2021 街上最亮的位置

路灯 `lights[i] = [position, range]` 照亮闭区间 `[position - range, position + range]`，返回被最多路灯照到的位置（并列取最小）。`1 <= lights.length <= 10^5`，`|position| <= 10^8`，`0 <= range <= 10^8`。

```python
from collections import defaultdict
def brightest_position(lights: list[list[int]]) -> int:
    diff: defaultdict[int, int] = defaultdict(int)   # 差分：在坐标 x 处亮度变化多少
    for pos, rng in lights:
        diff[pos - rng] += 1                     # 灯照亮 [pos-rng, pos+rng]：左端 +1
        diff[pos + rng + 1] -= 1                 # 右端的下一格 -1
    best = cur = 0
    ans = 0
    for x in sorted(diff):                       # 亮度只在有事件的坐标处变化，按坐标从小到大扫
        cur += diff[x]
        if cur > best:                           # 严格大于：并列时保留坐标更小的
            best, ans = cur, x
    return ans
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

**例题：** LC 2640 一个数组所有前缀的分数

定义 `conver[i] = arr[i] + max(arr[0..i])`，`arr` 的分数是 `conver` 之和。返回 `nums` 每个前缀的分数。`1 <= nums.length <= 10^5`，`1 <= nums[i] <= 10^9`。

```python
from itertools import accumulate
def find_prefix_score(nums: list[int]) -> list[int]:
    prefix_max = accumulate(nums, max)                    # 前缀最大值：max(nums[0..i])
    conver = (x + m for x, m in zip(nums, prefix_max))    # 转换数组 conver[i] = nums[i] + max(nums[0..i])
    return list(accumulate(conver))                       # 前缀分数 = conver 的前缀和
```

**例题：** LC 2145 统计隐藏数组数目

`differences[i] = hidden[i + 1] - hidden[i]`，隐藏数组所有数都在 `[lower, upper]` 内，求可能的隐藏数组个数。`1 <= n <= 10^5`，`|differences[i]|, |lower|, |upper| <= 10^5`。

```python
from itertools import accumulate
def number_of_arrays(differences: list[int], lower: int, upper: int) -> int:
    prefix = [0, *accumulate(differences)]     # hidden[i] = hidden[0] + prefix[i]，别漏掉开头的 0
    spread = max(prefix) - min(prefix)         # 数组内最大值与最小值之差，由 differences 唯一确定
    return max(0, (upper - lower) - spread + 1)   # 起点 hidden[0] 在区间内能平移多少个位置
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
