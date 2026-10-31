---
id: tlc-patterns-binary-search-1-signals
node: patterns.binary-search
type: qa
step: 1
---
## Q
**二分查找（Binary Search）｜信号**

什么样的题面该想到二分？「在下标上二分」和「对答案二分」分别由什么信号触发？哪些近似信号其实不能二分？

## A
**在下标上二分（数组本身有某种单调结构）：**
- 数组**有序**，要找值、找边界、找插入位置（例：LC 34 在排序数组中查找元素的第一个和最后一个位置）。
- 题面写明「时间复杂度 `O(log n)`」：LC 33、153、162、540 都有这句话（例：LC 162 寻找峰值；高频：LC 33 搜索旋转排序数组）。
- **旋转有序**数组、**峰值**、「只出现一次的数」：虽然整体不有序，但每次能判断答案在哪一半（例：LC 153 寻找旋转排序数组中的最小值）。

**对答案二分（答案在一个范围里，且可行性单调）：**
- 「**最小化最大值**」「**最大化最小值**」：LC 1011（最低运载能力）、LC 875（最小速度）（例：LC 875 爱吃香蕉的珂珂）。
- 「能否在 `x` 以内完成」判断函数容易写出来，且 `x` 越大（或越小）越容易 → 单调（例：LC 1802 有界数组中指定下标处的最大值；高频：LC 1918 第 K 小的子数组和）。
- 答案是整数，范围已知（`1..max`），第 `k` 小 / 大（LC 378 值域二分）、`sqrt`（LC 69）（例：LC 1539 第 k 个缺失的正整数；高频：LC 378 有序矩阵中第 K 小的元素）。

**共同点**：存在一个**判定函数** `ok(x)`，结果是 `False...False True...True`，要找第一个 `True`；每次判定后能丢掉一半。

**近似信号：**
- 数组无序，没有单调结构 → 先排序再二分，或哈希：按结束时间排序后，对每份兼职二分找上一份不冲突的兼职（例：LC 1235 规划兼职工作）。
- 判定函数**不单调**（`x` 变大时可行性忽好忽坏）→ 不能二分，可能是 DP：「前 `x` 个字符能否拆分」没有单调性（例：LC 139 单词拆分）。
- 要找**所有**满足条件的位置 → 找边界后线性输出，或直接用两个边界的下标差得到个数（例：LC 2300 咒语和药水的成功对数）。
- 值域极大但判定函数是 `O(n)` 或 `O(1)`：二分次数是 `log(值域)`，总 `O(n log 值域)`，这是它依然可行的原因：`x` 到 `2^31 - 1` 也只要 31 轮（例：LC 69 x 的平方根）。

**例题：** LC 34 在排序数组中查找元素的第一个和最后一个位置

给一个按**非递减**顺序排列的整数数组 `nums` 和目标值 `target`，找出 `target` 在数组中的开始位置和结束位置，不存在则返回 `[-1, -1]`。必须设计并实现时间复杂度 `O(log n)` 的算法。`0 <= nums.length <= 10^5`，`-10^9 <= nums[i] <= 10^9`，`-10^9 <= target <= 10^9`。

```python
from bisect import bisect_left, bisect_right

def search_range(nums: list[int], target: int) -> list[int]:
    lo = bisect_left(nums, target)          # 第一个 >= target 的位置
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]                     # 越界或该位置不是 target：不存在
    hi = bisect_right(nums, target) - 1     # 第一个 > target 的位置再减 1 = 最后一个 target
    return [lo, hi]
```

**例题：** LC 162 寻找峰值

找到一个严格大于左右相邻值的峰值元素并返回其下标（有多个峰值时返回任意一个，`nums[-1] = nums[n] = -∞`），必须是 `O(log n)`。`1 <= nums.length <= 1000`，相邻元素不相等。

```python
def find_peak_element(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1          # 在闭区间 [lo, hi] 里一定还有峰值
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:  # 上坡：右边一定有峰（最坏一路爬到最右端）
            lo = mid + 1
        else:                          # 下坡：mid 自己或左边有峰（相邻不相等）
            hi = mid
    return lo
```

**例题：** LC 153 寻找旋转排序数组中的最小值

一个元素**互不相同**的升序数组，经过 `1` 到 `n` 次旋转得到 `nums`（旋转一次是把最后一个元素移到最前面，例如 `[0,1,2,4,5,6,7]` 旋转 `4` 次得到 `[4,5,6,7,0,1,2]`，旋转 `n` 次回到原数组）。找出并返回最小元素，必须是 `O(log n)`。`1 <= n <= 5000`，`-5000 <= nums[i] <= 5000`，元素互不相同。

```python
def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:                      # 区间收缩到一个元素时，它就是最小值
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:        # 断崖在 mid 右边，最小值在 (mid, hi]
            lo = mid + 1
        else:                           # mid 已在右半段，最小值在 [lo, mid]
            hi = mid
    return nums[lo]
```

**例题：** LC 875 爱吃香蕉的珂珂

有 `n` 堆香蕉，第 `i` 堆有 `piles[i]` 根。警卫离开，`h` 小时后回来。珂珂决定吃香蕉的速度 `k`（根/小时）：每小时选一堆，吃掉 `k` 根；这堆不足 `k` 根就全吃完，这一小时不再吃别的。求能在 `h` 小时内吃完所有香蕉的**最小**整数速度 `k`。`1 <= piles.length <= 10^4`，`piles.length <= h <= 10^9`，`1 <= piles[i] <= 10^9`。

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    lo, hi = 1, max(piles)                  # 答案在 [1, max(piles)]
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum((p + mid - 1) // mid for p in piles)   # 向上取整
        if hours <= h:
            hi = mid                        # mid 够快，答案在 [lo, mid]
        else:
            lo = mid + 1                    # mid 太慢，答案在 (mid, hi]
    return lo
```

**例题：** LC 1802 有界数组中指定下标处的最大值

给三个正整数 `n`、`index` 和 `maxSum`。构造数组 `nums`（下标从 `0` 开始），同时满足：`nums.length == n`；每个 `nums[i]` 都是**正整数**；相邻元素之差的绝对值不超过 `1`，即 `abs(nums[i] - nums[i+1]) <= 1`；所有元素之和不超过 `maxSum`；`nums[index]` 的值被**最大化**。返回所构造数组中的 `nums[index]`。`1 <= n <= maxSum <= 10^9`，`0 <= index < n`。

```python
def max_value(n: int, index: int, max_sum: int) -> int:
    def side(peak: int, length: int) -> int:
        if length >= peak - 1:
            return peak * (peak - 1) // 2 + (length - (peak - 1))
        return (peak - 1 + peak - length) * length // 2
    def total(peak: int) -> int:               # 峰值取 peak 时整个数组的最小和
        return peak + side(peak, index) + side(peak, n - 1 - index)
    lo, hi = 1, max_sum                        # 单调：peak 越大 total 越大
    while lo < hi:
        mid = (lo + hi + 1) // 2               # 上取整，避免 lo = mid 时死循环
        if total(mid) <= max_sum:
            lo = mid                           # mid 放得下，答案至少是 mid
        else:
            hi = mid - 1
    return lo
```

**例题：** LC 1539 第 k 个缺失的正整数

给一个**严格升序**排列的正整数数组 `arr` 和整数 `k`，找出这个数组里缺失的第 `k` 个正整数。`1 <= arr.length <= 1000`，`1 <= arr[i] <= 1000`，`1 <= k <= 1000`，对所有 `i < j` 有 `arr[i] < arr[j]`。进阶：设计时间复杂度小于 `O(n)` 的算法。

```python
def find_kth_positive(arr: list[int], k: int) -> int:
    lo, hi = 0, len(arr)                   # 在 [0, n] 上找第一个下标 i，使 arr[i] 之前缺失的数 >= k
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) >= k:      # arr[mid] 之前缺了 arr[mid] - (mid + 1) 个正整数
            hi = mid
        else:
            lo = mid + 1
    return lo + k                          # 答案前面有 lo 个数在 arr 里：第 k 个缺失数 = k + lo
```

**例题：** LC 1235 规划兼职工作

有 `n` 份兼职工作，第 `i` 份从 `startTime[i]` 开始、`endTime[i]` 结束，报酬 `profit[i]`。时间上重叠的两份工作不能同时做；在时间 `X` 结束的工作，可以立刻接在 `X` 开始的下一份。求能获得的最大报酬。`1 <= n <= 5 * 10^4`，`1 <= startTime[i] < endTime[i] <= 10^9`，`1 <= profit[i] <= 10^4`。

```python
def job_scheduling(start_time: list[int], end_time: list[int], profit: list[int]) -> int:
    jobs = sorted(zip(end_time, start_time, profit))     # 按结束时间排序
    ends = [end for end, _, _ in jobs]
    dp = [0] * (len(jobs) + 1)                           # dp[i]：只考虑前 i 份工作的最大报酬
    for i, (end, start, gain) in enumerate(jobs):
        # 结束时间 <= start 的工作有 k 份，正是排序后的前 k 份；end > start，所以 k <= i
        k = bisect_right(ends, start, 0, i)
        dp[i + 1] = max(dp[i], dp[k] + gain)             # 不做这份 / 做这份
    return dp[-1]
```

**例题：** LC 139 单词拆分

给字符串 `s` 和字符串列表 `wordDict`（字典）。如果能用字典里的一个或多个单词拼接出 `s` 就返回 `true`；单词可以重复使用，也不要求用完字典。`1 <= s.length <= 300`，`1 <= wordDict.length <= 1000`，`1 <= wordDict[i].length <= 20`，`s` 和单词都只含小写字母，字典里的单词互不相同。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)                       # 哈希集合：判断"切片是不是单词"是 O(L)
    max_len = max(map(len, words))               # 单词最长 max_len，更长的切片不用试
    dp = [True] + [False] * len(s)               # dp[i]：前 i 个字符 s[:i] 能否被拆成单词
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**例题：** LC 2300 咒语和药水的成功对数

给两个正整数数组 `spells`（长度 `n`）和 `potions`（长度 `m`），`spells[i]` 是第 `i` 个咒语的能量，`potions[j]` 是第 `j` 瓶药水的能量，再给整数 `success`。咒语和药水的能量**相乘**大于等于 `success`，就是一对「成功」的组合。返回长度为 `n` 的数组 `pairs`，`pairs[i]` 是能与第 `i` 个咒语成功组合的药水数量。`1 <= n, m <= 10^5`，`1 <= spells[i], potions[j] <= 10^5`，`1 <= success <= 10^10`。

```python
from bisect import bisect_left


def successful_pairs(spells: list[int], potions: list[int], success: int) -> list[int]:
    potions = sorted(potions)
    m = len(potions)
    # 对每个咒语 s：在有序药水里找第一个满足 p * s >= success 的位置，其右边全部成功
    return [m - bisect_left(potions, success, key=lambda p: p * s) for s in spells]
```

**例题：** LC 69 x 的平方根

给非负整数 `x`，返回 `x` 的算术平方根，结果只保留整数部分（向下取整）。不允许使用内置的指数函数和运算符，如 `pow(x, 0.5)` 或 `x ** 0.5`。`0 <= x <= 2^31 - 1`。

```python
def my_sqrt(x: int) -> int:
    lo, hi = 0, x                                  # 答案 m 满足 m*m <= x，找最大的这样的 m
    while lo < hi:
        mid = (lo + hi + 1) // 2                   # 向上取整，否则 lo = mid 时区间不缩小会死循环
        if mid * mid <= x:
            lo = mid                               # mid 可行：答案至少是 mid
        else:
            hi = mid - 1
    return lo
```

**例题：** LC 33 搜索旋转排序数组

整数数组 `nums` 原本按升序排列且值**互不相同**，在某个未知的下标 `k`（`0 <= k < nums.length`）处向左旋转，变成 `[nums[k], nums[k+1], ..., nums[n-1], nums[0], ..., nums[k-1]]`。给旋转后的 `nums` 和目标值 `target`，返回 `target` 的下标，不存在返回 `-1`，要求 `O(log n)`。`1 <= nums.length <= 5000`，`-10^4 <= nums[i] <= 10^4`，`nums` 中每个值都独一无二，`-10^4 <= target <= 10^4`。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                  # 左半 [lo, mid] 是有序的
            if nums[lo] <= target < nums[mid]:     # target 落在有序的左半里：去左边
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                      # 否则右半 [mid, hi] 一定有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**例题：** LC 1918 第 K 小的子数组和

给长度为 `n` 的整数数组 `nums` 和整数 `k`，返回**第 `k` 小的子数组和**。子数组是数组中非空且连续的一段，子数组和是其中所有元素之和（不同位置的子数组即使和相同也各算一个）。`1 <= n <= 2 * 10^4`，`1 <= nums[i] <= 5 * 10^4`，`1 <= k <= n * (n + 1) / 2`。

```python
def kth_smallest_subarray_sum(nums: list[int], k: int) -> int:
    def count_le(x: int) -> int:                  # 和 <= x 的子数组个数（元素全为正，双指针）
        cnt = left = cur = 0
        for right, v in enumerate(nums):
            cur += v
            while cur > x:                        # 窗口和超标：收缩左端
                cur -= nums[left]
                left += 1
            cnt += right - left + 1               # 以 right 结尾、左端在 [left, right] 的子数组都 <= x
        return cnt

    lo, hi = min(nums), sum(nums)                 # 答案一定落在 [最小元素, 总和]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:                    # 至少 k 个子数组 <= mid：答案 <= mid
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**例题：** LC 378 有序矩阵中第 K 小的元素

`n × n` 矩阵 `matrix`，每行每列都按非递减顺序排列。找到矩阵中**排序后**的第 `k` 小的元素（重复的值各算一个，不是第 `k` 个不同的值）。要求内存复杂度优于 `O(n^2)`。`1 <= n <= 300`，`-10^9 <= matrix[i][j] <= 10^9`，`1 <= k <= n^2`。

```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)

    def count_le(mid: int) -> int:             # 矩阵中 <= mid 的元素个数，阶梯式 O(n)
        count, col = 0, n - 1
        for row in matrix:                     # 行从上到下，每行的列边界只会左移
            while col >= 0 and row[col] > mid:
                col -= 1
            count += col + 1
        return count

    lo, hi = matrix[0][0], matrix[-1][-1]      # 答案一定落在 [最小值, 最大值]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:                 # 至少有 k 个数 <= mid：答案 <= mid
            hi = mid
        else:
            lo = mid + 1
    return lo
```
