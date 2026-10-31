---
id: tlc-patterns-prefix-sum-5-variants
node: patterns.prefix-sum
type: qa
step: 5
---
## Q
**前缀和与差分（Prefix Sum）｜变形：二维前缀和、扫描线、前缀最值、值域差分**

二维前缀和怎么算？「最亮的位置」类的覆盖计数怎么用差分？隐藏数组计数（LC 2145）和前缀分数（LC 2640）里前缀和起什么作用？

## A
**二维前缀和**：`p[r+1][c+1]` = 左上角到 `(r, c)` 的矩形和，容斥原理（例：LC 1074 元素和为目标值的子矩阵数量；高频：LC 560 和为 K 的子数组）。

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

**LC 2021 最亮的位置**：坐标很大，用字典做稀疏差分，排序后扫描（例：LC 2021 街上最亮的位置）：

```python
from collections import Counter
def brightest_position(lights: list[list[int]]) -> int:
    diff: Counter[int] = Counter()
    for p, r in lights:
        diff[p - r] += 1
        diff[p + r + 1] -= 1          # 闭区间 [p-r, p+r]，结束点后一位撤掉
    best = cur = ans = 0
    for pos in sorted(diff):
        cur += diff[pos]
        if cur > best:                # 严格大于：同亮度取最小坐标
            best, ans = cur, pos
    return ans
print(brightest_position([[-3, 2], [1, 2], [3, 3]]), brightest_position([[1, 0], [0, 1]]), brightest_position([[1, 2]]))   # -1 1 -1
```

- **LC 2145**：`pre = [0, *accumulate(differences)]` 是隐藏数组相对起点的偏移。可行起点个数 = `(upper - lower) - (max(pre) - min(pre)) + 1`，不小于 0（例：LC 2145 统计隐藏数组数目）。
- **LC 2640**：边扫边维护前缀最大值与累计和，`ans[i]` = 之前累计 + `nums[i] + 当前最大`（例：LC 2640 一个数组所有前缀的分数）。
- **LC 209**：元素全为正 → 前缀和严格递增 → `bisect_left(pre, pre[i] + target)` 找右端，`O(n log n)`（例：LC 209 长度最小的子数组）。

**例题：** LC 1074 元素和为目标值的子矩阵数量

`m x n` 整数矩阵（`1 <= m, n <= 100`，`-1000 <= v <= 1000`）和目标值 `target`，统计元素和等于 `target` 的非空子矩阵个数。

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

**例题：** LC 2021 街上最亮的位置

`lights[i] = [position, range]`（至多 `10^5` 盏，`-10^8 <= position <= 10^8`，`0 <= range <= 10^8`）表示路灯照亮闭区间 `[position - range, position + range]`；位置的亮度是照到它的路灯数。返回最亮的位置，并列时取坐标最小的。

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

**例题：** LC 2145 统计隐藏数组数目

隐藏数组 `hidden` 长度为 `n + 1`（`1 <= n <= 10^5`），已知相邻差值数组 `differences`，且 `hidden` 的所有值都在闭区间 `[lower, upper]` 内，求符合要求的隐藏数组个数。

```python
from itertools import accumulate
def number_of_arrays(differences: list[int], lower: int, upper: int) -> int:
    prefix = [0, *accumulate(differences)]     # hidden[i] = hidden[0] + prefix[i]，别漏掉开头的 0
    spread = max(prefix) - min(prefix)         # 数组内最大值与最小值之差，由 differences 唯一确定
    return max(0, (upper - lower) - spread + 1)   # 起点 hidden[0] 在区间内能平移多少个位置
```

**例题：** LC 2640 一个数组所有前缀的分数

数组 `arr` 的转换数组 `conver[i] = arr[i] + max(arr[0..i])`，分数是 `conver` 所有元素之和。给定 `nums`（`1 <= n <= 10^5`，`1 <= v <= 10^9`），返回每个前缀 `nums[0..i]` 的分数。

```python
from itertools import accumulate
def find_prefix_score(nums: list[int]) -> list[int]:
    prefix_max = accumulate(nums, max)                    # 前缀最大值：max(nums[0..i])
    conver = (x + m for x, m in zip(nums, prefix_max))    # 转换数组 conver[i] = nums[i] + max(nums[0..i])
    return list(accumulate(conver))                       # 前缀分数 = conver 的前缀和
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
