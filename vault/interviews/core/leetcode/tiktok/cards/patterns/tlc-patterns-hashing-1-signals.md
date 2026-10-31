---
id: tlc-patterns-hashing-1-signals
node: patterns.hashing
type: qa
step: 1
---
## Q
**哈希（Hashing）｜信号**

什么样的题面该想到哈希表？有哪些长得像、实际上要用排序、双指针或前缀和的近似信号？

## A
**该想到哈希的信号：**
- 内层循环是「找有没有一个值」：找 `target - x`、找「之前出现过的」、找重复 → 把内层 `O(n)` 查找换成 `O(1)`（例：LC 1 两数之和）。
- 要**统计次数**、判断「出现次数是否相同」、比较两个多重集 → `Counter`（例：LC 242 有效的字母异位词；高频：LC 438 找到字符串中所有字母异位词）。
- 要把元素按某个**签名（signature）**分组：排序后的字符串、计数向量、归一化的形状 → `defaultdict(list)`（例：LC 49 字母异位词分组）。
- 要**去重**或判断是否见过 → `set`（例：LC 217 存在重复元素）。
- 数据范围到 `10^5`，暴力是 `O(n^2)`，且顺序不重要（例：LC 128 最长连续序列）。

**近似信号（要换别的）：**
- 要保持**有序**、找前驱 / 后继 → 有序结构或排序 + 二分，哈希不记顺序（例：LC 35 搜索插入位置）。
- 数组**已有序**，找两数之和 → 双指针，`O(1)` 空间，不用哈希（例：LC 167 两数之和 II - 输入有序数组；高频：LC 15 三数之和）。
- 问的是**连续子数组**的和 / 个数 → 前缀和 + 哈希（哈希只是其中一半）（例：LC 560 和为 K 的子数组）。
- 键是**范围**（`x` 落在 `[l, r]`）→ 排序 / 二分 / 区间结构（例：LC 56 合并区间）。
- 键是浮点数 → 哈希不可靠（精度），改用整数化或排序（例：LC 149 直线上最多的点数）。

**代价**：平均 `O(1)`，空间 `O(n)`；最坏情况（大量哈希冲突）退化，但 Python 的 `int` 与 `str` 哈希足够好，面试里不必担心。

**例题：** LC 1 两数之和

整数数组 `nums`（`2 <= nums.length <= 10^4`）和目标值 `target`，返回和为 `target` 的两个元素的下标，恰有一个答案，同一元素不能用两次。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}                  # 值 -> 下标
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:   # 先查：只会匹配到前面的元素
            return [j, i]
        seen[x] = i                            # 后存：自己不会和自己配对
    return []
```

**例题：** LC 242 有效的字母异位词

给定字符串 `s` 和 `t`（长度都不超过 `5 * 10^4`，仅含小写字母），判断 `t` 是否是 `s` 的字母异位词。

```python
from collections import Counter
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):                 # 长度不同直接否；也是下面「没出现负数」能推出「全为 0」的前提
        return False
    count = Counter(s)                   # 字符 -> 它在 s 里的出现次数
    for ch in t:
        count[ch] -= 1
        if count[ch] < 0:                # t 里的 ch 比 s 多
            return False
    return True
```

**例题：** LC 49 字母异位词分组

字符串数组 `strs`（`1 <= strs.length <= 10^4`，每个长度不超过 100，仅小写字母），把字母异位词放在一组，组的顺序不限。

```python
from collections import defaultdict
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # 26 个字母的出现次数就是指纹
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # list 不可哈希，转成 tuple 才能当键
    return list(groups.values())
```

**例题：** LC 217 存在重复元素

整数数组 `nums`（`1 <= nums.length <= 10^5`），判断是否有某个值至少出现两次。

```python
def contains_duplicate(nums: list[int]) -> bool:
    seen: set[int] = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**例题：** LC 128 最长连续序列

未排序整数数组 `nums`（`0 <= nums.length <= 10^5`），求数字连续的最长序列的长度（元素在原数组中不必相邻），要求 `O(n)`。

```python
def longest_consecutive(nums: list[int]) -> int:
    seen = set(nums)                   # 去重 + O(1) 查询
    best = 0
    for x in seen:
        if x - 1 in seen:              # x 不是序列的起点：跳过，让起点去数
            continue
        end = x + 1
        while end in seen:             # 从起点向右数下去
            end += 1
        best = max(best, end - x)
    return best
```

**例题：** LC 35 搜索插入位置

升序、无重复的整数数组 `nums`（`1 <= nums.length <= 10^4`）和目标值 `target`，返回目标值的下标；不存在则返回它应插入的位置，要求 `O(log n)`。

```python
def search_insert(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)                    # 答案区间 [lo, hi]，hi 可以等于 len(nums)（插到末尾）
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1                     # mid 和它左边都 < target，答案在右边
        else:
            hi = mid                         # mid 可能就是答案，保留
    return lo
```

**例题：** LC 167 两数之和 II - 输入有序数组

非递减数组 `numbers`（`2 <= numbers.length <= 3 * 10^4`，下标从 1 开始）和 `target`，返回和为 `target` 的两个 1-based 下标，答案唯一，只能用常数额外空间。

```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

**例题：** LC 56 合并区间

区间数组 `intervals`（`1 <= intervals.length <= 10^4`，`0 <= start <= end <= 10^4`），合并所有重叠区间，返回不重叠且恰好覆盖全部输入的区间数组。

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    merged: list[list[int]] = []
    for start, end in sorted(intervals):           # 按起点排序；起点相同按终点，不影响结果
        if merged and start <= merged[-1][1]:      # 与上一个区间重叠（端点相接也算）
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**例题：** LC 149 直线上最多的点数

给平面上 `n` 个互不相同的点 `points`（`1 <= n <= 300`，`-10^4 <= x, y <= 10^4`），求同一条直线上最多有多少个点。

```python
from collections import Counter
from math import gcd
def max_points(points: list[list[int]]) -> int:
    best = 1
    for i, (x1, y1) in enumerate(points):
        slopes: Counter[tuple[int, int]] = Counter()
        for x2, y2 in points[i + 1:]:
            dx, dy = x2 - x1, y2 - y1
            g = gcd(dx, dy)                    # 点互不相同，所以 g > 0
            dx, dy = dx // g, dy // g          # 约分成最简整数方向向量，不用浮点斜率当键
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy              # 统一方向：(1, 2) 与 (-1, -2) 是同一条线
            slopes[(dx, dy)] += 1
        if slopes:
            best = max(best, max(slopes.values()) + 1)   # 加上点 i 自己
    return best
```

**例题：** LC 438 找到字符串中所有字母异位词

给两个字符串 `s` 和 `p`（长度都在 `1` 到 `3 * 10^4`，只含小写字母），返回 `s` 中所有是 `p` 的异位词（字母相同、次序可以不同）的子串的起始下标，顺序任意。

```python
def find_anagrams(s: str, p: str) -> list[int]:
    m = len(p)
    need = Counter(p)
    unbalanced = len(need)
    ans: list[int] = []
    def shift(c: str, d: int) -> int:
        """窗口增减一个 c，返回 unbalanced 的变化量。"""
        was = need[c] != 0
        need[c] += d
        return (need[c] != 0) - was
    for right, ch in enumerate(s):
        unbalanced += shift(ch, -1)
        if right >= m:
            unbalanced += shift(s[right - m], +1)
        if unbalanced == 0:
            ans.append(right - m + 1)
    return ans
```

**例题：** LC 15 三数之和

给整数数组 `nums`，返回所有和为 `0` 且**不重复**的三元组 `[nums[i], nums[j], nums[k]]`，要求 `i`、`j`、`k` 互不相同；答案中不能包含重复的三元组，顺序不限。`3 <= nums.length <= 3000`，`-10^5 <= nums[i] <= 10^5`。

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    result: list[list[int]] = []
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
    return result
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
