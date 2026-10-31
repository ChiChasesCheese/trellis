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
- 要**统计次数**、判断「出现次数是否相同」、比较两个多重集 → `Counter`（例：LC 242 有效的字母异位词）。
- 要把元素按某个**签名（signature）**分组：排序后的字符串、计数向量、归一化的形状 → `defaultdict(list)`（例：LC 49 字母异位词分组）。
- 要**去重**或判断是否见过 → `set`（例：LC 217 存在重复元素）。
- 数据范围到 `10^5`，暴力是 `O(n^2)`，且顺序不重要（例：LC 128 最长连续序列）。

**近似信号（要换别的）：**
- 要保持**有序**、找前驱 / 后继 → 有序结构或排序 + 二分，哈希不记顺序（例：LC 35 搜索插入位置）。
- 数组**已有序**，找两数之和 → 双指针，`O(1)` 空间，不用哈希（例：LC 167 两数之和 II - 输入有序数组）。
- 问的是**连续子数组**的和 / 个数 → 前缀和 + 哈希（哈希只是其中一半）（例：LC 523 连续的子数组和）。
- 键是**范围**（`x` 落在 `[l, r]`）→ 排序 / 二分 / 区间结构（例：LC 56 合并区间）。
- 键是浮点数 → 哈希不可靠（精度），改用整数化或排序（例：LC 593 有效的正方形）。

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

**例题：** LC 523 连续的子数组和

非负整数数组 `nums`（`1 <= nums.length <= 10^5`）和整数 `k`（`1 <= k <= 2^31 - 1`），判断是否存在长度至少为 2、元素和为 `k` 倍数的连续子数组。

```python
def check_subarray_sum(nums: list[int], k: int) -> bool:
    first_seen: dict[int, int] = {0: -1}     # 余数 -> 最早出现的前缀下标；空前缀的余数是 0
    prefix = 0
    for i, x in enumerate(nums):
        prefix = (prefix + x) % k            # 到 nums[i] 为止的前缀和对 k 的余数
        j = first_seen.setdefault(prefix, i)  # 第一次出现就登记 i，否则返回最早的下标
        if i - j >= 2:                       # 子数组 nums[j+1 .. i] 的长度 = i - j
            return True
    return False
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

**例题：** LC 593 有效的正方形

给定二维平面上的四个点 `p1..p4`（坐标范围 `-10^4..10^4`，顺序任意），判断它们能否构成正方形。

```python
from itertools import combinations
def valid_square(p1: list[int], p2: list[int], p3: list[int], p4: list[int]) -> bool:
    def dist2(a: list[int], b: list[int]) -> int:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2   # 平方距离，全程整数
    d = sorted(dist2(a, b) for a, b in combinations((p1, p2, p3, p4), 2))   # 6 条两两距离
    return d[0] > 0 and d[0] == d[3] and d[4] == d[5] == 2 * d[0]
```
