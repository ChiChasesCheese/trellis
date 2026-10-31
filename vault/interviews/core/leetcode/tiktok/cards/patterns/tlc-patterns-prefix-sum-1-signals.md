---
id: tlc-patterns-prefix-sum-1-signals
node: patterns.prefix-sum
type: qa
step: 1
---
## Q
**前缀和与差分（Prefix Sum）｜信号**

什么样的题面该想到前缀和，什么样该想到差分？哪些近似信号其实要滑动窗口或别的方法？

## A
**前缀和（Prefix Sum）的信号：**
- 反复求**区间 `[l, r]` 的和**（或异或、乘积、计数），暴力每次 `O(n)` → 预处理 `pre`，每次 `O(1)`（例：LC 1352 最后 K 个数的乘积）。
- 问**连续子数组**的和等于 / 被 `k` 整除的**个数**或存在性 → `pre[j] - pre[i] = k`，在哈希表里找 `pre[i] = pre[j] - k`（例：LC 974 和可被 K 整除的子数组）。
- **数组含负数**，不能用滑动窗口（右端增大和不一定增大）：把 `0` 记成 `-1` 后，窗口和忽大忽小（例：LC 525 连续数组；高频：LC 560 和为 K 的子数组）。
- 「**恰好**有 `k` 个奇数 / 1」→ 把元素映射成 0/1，再按子数组和 = `k` 处理（例：LC 1248 统计「优美子数组」）。
- 二维矩阵的子矩阵和 → 二维前缀和（例：LC 1074 元素和为目标值的子矩阵数量）。

**差分（Difference Array）的信号：**
- 对很多个区间**批量加减**同一个值，最后一次性读出每个位置 → 差分，更新 `O(1)`，还原 `O(n)`（例：LC 1094 拼车）。
- 「某点被几个区间覆盖」「最亮的位置」「航班预订」→ 差分 / 扫描线（例：LC 2021 街上最亮的位置）。

**近似信号：**
- 全是**正数**，求和**至少** `target` 的最短子数组 → 滑动窗口 `O(n)`（LC 209），前缀和 + 二分是另一种 `O(n log n)`（例：LC 209 长度最小的子数组）。
- 只问**最大**子数组和（不计数）→ Kadane / DP，不需要哈希（例：LC 53 最大子数组和）。
- 需要区间**最大值**而非和 → 稀疏表、单调队列，前缀和做不了（例：LC 239 滑动窗口最大值）。
- 要**修改**元素再查询 → 树状数组 / 线段树，前缀和是静态的。

**例题：** LC 1352 最后 K 个数的乘积

设计一个接受整数流并能查询最后 `k` 个整数乘积的类 `ProductOfNumbers`：`add(num)` 把 `num` 添加到数字列表末尾；`getProduct(k)` 返回当前列表中最后 `k` 个数字的乘积（保证列表中至少有 `k` 个数字）。任何时候，任意连续数字序列的乘积都在 32 位整数范围内。`0 <= num <= 100`，`1 <= k <= 4 * 10^4`，`add` 与 `getProduct` 合计最多调用 `4 * 10^4` 次。进阶：让 `getProduct` 和 `add` 都是 `O(1)`。

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

**例题：** LC 974 和可被 K 整除的子数组

给整数数组 `nums` 和整数 `k`，返回元素之和可被 `k` 整除的**非空连续子数组**的个数。`1 <= nums.length <= 3 * 10^4`，`-10^4 <= nums[i] <= 10^4`，`2 <= k <= 10^4`。

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

**例题：** LC 525 连续数组

给一个二进制数组 `nums`（每个元素不是 `0` 就是 `1`），求含有**相同数量的 `0` 和 `1`** 的最长连续子数组的长度。`1 <= nums.length <= 10^5`。

```python
def find_max_length(nums: list[int]) -> int:
    first: dict[int, int] = {0: -1}      # 前缀差值 -> 它第一次出现的下标；空前缀记在 -1
    best = bal = 0                       # bal = 前缀里 1 的个数减 0 的个数
    for i, x in enumerate(nums):
        bal += 1 if x else -1            # 把 0 看成 -1
        if bal in first:                 # 两个前缀差值相同：中间那段 0 和 1 一样多
            best = max(best, i - first[bal])
        else:
            first[bal] = i               # 只记第一次出现，子数组才最长
    return best
```

**例题：** LC 1248 统计「优美子数组」

给整数数组 `nums` 和整数 `k`。如果某个连续子数组中**恰好**有 `k` 个奇数，就称它为「优美子数组」。返回数组中优美子数组的数目。`1 <= nums.length <= 50000`，`1 <= nums[i] <= 10^5`，`1 <= k <= nums.length`。

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

**例题：** LC 1074 元素和为目标值的子矩阵数量

给一个矩阵 `matrix` 和目标值 `target`，返回元素总和等于 `target` 的**非空子矩阵**的数量。子矩阵由 `(x1, y1, x2, y2)` 决定，包含所有满足 `x1 <= x <= x2`、`y1 <= y <= y2` 的单元 `matrix[x][y]`；只要有一个坐标不同就算不同的子矩阵。`1 <= matrix.length, matrix[0].length <= 100`，`-1000 <= matrix[i][j] <= 1000`，`-10^8 <= target <= 10^8`。

```python
from collections import Counter
def num_submatrix_sum_target(matrix: list[list[int]], target: int) -> int:
    m, n = len(matrix), len(matrix[0])
    ans = 0
    for top in range(m):
        col = [0] * n                      # col[c]：第 top..bottom 行、第 c 列的和
        for bottom in range(top, m):
            col = [a + b for a, b in zip(col, matrix[bottom])]
            seen = Counter({0: 1})         # 前缀和 -> 出现次数；空前缀和为 0
            s = 0
            for v in col:                  # 把 col 当一维数组：数和为 target 的子数组
                s += v
                ans += seen[s - target]    # 以当前列结尾、前缀和为 s - target 的起点个数
                seen[s] += 1
    return ans
```

**例题：** LC 1094 拼车

车有 `capacity` 个座位且只能往一个方向开；`trips[i] = [人数, 上车里程, 下车里程]`，同一位置先下后上。判断途中任意一点是否都不超载。`1 <= trips.length <= 1000`，`0 <= from < to <= 1000`，`1 <= capacity <= 10^5`。

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    change = [0] * 1001  # 里程 0..1000 上的人数变化量
    for passengers, start, end in trips:
        change[start] += passengers
        change[end] -= passengers
    current = 0
    for delta in change:
        current += delta
        if current > capacity:
            return False
    return True
```

**例题：** LC 2021 街上最亮的位置

一条街上有许多路灯，路灯的坐标由数组 `lights` 给出：`lights[i] = [position, range]` 表示坐标为 `position` 的路灯照亮闭区间 `[position - range, position + range]`。位置 `p` 的亮度等于能照到 `p` 的路灯数量。返回最亮的位置；有多个时返回坐标最小的。`1 <= lights.length <= 10^5`，`-10^8 <= position <= 10^8`，`0 <= range <= 10^8`。

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

**例题：** LC 209 长度最小的子数组

给一个含 `n` 个**正整数**的数组 `nums` 和一个正整数 `target`，找出和大于等于 `target` 的长度最小的连续子数组，返回它的长度；不存在则返回 `0`。`1 <= target <= 10^9`，`1 <= nums.length <= 10^5`，`1 <= nums[i] <= 10^4`。进阶：做出 `O(n)` 解后，再设计一个 `O(n log n)` 的解。

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

**例题：** LC 53 最大子数组和

给整数数组 `nums`，找出一个具有最大和的**连续子数组**（至少包含一个元素），返回其最大和。`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`。

```python
from itertools import islice


def max_sub_array(nums: list[int]) -> int:
    best = cur = nums[0]                # cur：以当前元素结尾的最大子数组和
    for x in islice(nums, 1, None):     # 跳过首元素，又不拷贝切片
        cur = max(x, cur + x)           # 接在前面后面，或者从 x 重新开始
        best = max(best, cur)
    return best
```

**例题：** LC 239 滑动窗口最大值

大小为 `k` 的窗口从数组最左侧每次右移一位到最右侧，返回每个窗口位置上的最大值。`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`，`1 <= k <= nums.length`。

```python
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    window: deque[int] = deque()       # 存下标；对应的值从队首到队尾严格递减
    ans: list[int] = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()               # 比 x 小（或相等）且更靠左的数，永远没有机会当最大值
        window.append(i)
        if window[0] <= i - k:         # 队首已经滑出窗口
            window.popleft()
        if i >= k - 1:                 # 窗口满了才记录
            ans.append(nums[window[0]])
    return ans
```

**例题：** LC 560 和为 K 的子数组

整数数组 `nums`（含负数）和整数 `k`，返回和为 `k` 的连续子数组个数；`1 <= nums.length <= 2 * 10^4`，`-1000 <= nums[i] <= 1000`。

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
