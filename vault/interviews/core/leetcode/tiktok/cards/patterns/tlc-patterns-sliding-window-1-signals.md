---
id: tlc-patterns-sliding-window-1-signals
node: patterns.sliding-window
type: qa
step: 1
---
## Q
**滑动窗口（Sliding Window）｜信号**

什么样的题面该想到滑动窗口？固定窗口、可变窗口各自的信号是什么？哪些近似信号需要换方法？

## A
**共同信号**：对象是**连续**的子数组 / 子串，问的是**最长、最短或个数**，并且约束有**单调性**：窗口扩大后约束只会更难满足（或更容易满足）。

**可变窗口**：
- 「至多包含 `k` 种不同字符 / 至多替换 `k` 次的最长子串」→ 违反约束就缩左端（LC 340、424、904、3）（例：LC 340 至多包含 K 个不同字符的最长子串）。
- 「和不小于 `target` 的最短子数组」，元素全为正数 → 满足就缩左端（LC 209）（例：LC 209 长度最小的子数组）。
- 「包含 `t` 中所有字符的最短子串」→ 覆盖了再尽量缩（LC 76）（例：LC 76 最小覆盖子串）。

**固定窗口**：题面里直接给出窗口长度，或长度由输入确定：
- 「所有长度为 `m` 的异位词子串」LC 438（窗口长度 = `m`，由输入确定）（例：LC 438 找到字符串中所有字母异位词）。

**数据范围**：`n` 到 `10^5`，暴力 `O(n^2)` 不行，要求 `O(n)`（例：LC 1004 最大连续1的个数 III）。

**近似信号：**
- 含**负数**，求和相关 → 窗口不单调，改前缀和 + 哈希（LC 560）（例：LC 560 和为 K 的子数组）。
- 子**序列**（不要求连续）→ DP（例：LC 300 最长递增子序列）。
- 「**恰好** `k`」→ 直接窗口会漏，转成「至多 `k`」减「至多 `k-1`」（LC 1248）（例：LC 1248 统计「优美子数组」）。
- 窗口里要最大值 → 单调队列（LC 239），不是普通窗口（例：LC 239 滑动窗口最大值）。
- 约束不是单调的（例如「每个字符至少出现 `k` 次」LC 395）→ 枚举种类数 `1..26` 当外层，或分治（例：LC 395 至少有 K 个重复字符的最长子串）。

**例题：** LC 340 至多包含 K 个不同字符的最长子串

字符串 `s`（`1 <= length <= 5 * 10^4`）和 `k`（`0 <= k <= 50`），求至多包含 `k` 种不同字符的最长子串长度。

```python
from collections import Counter
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    count: Counter[str] = Counter()         # 窗口内每个字符的出现次数
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:               # 种类超了：缩左端，计数归零就删键，len 才准
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]
            left += 1
        best = max(best, right - left + 1)
    return best
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

**例题：** LC 76 最小覆盖子串

字符串 `s`、`t`（长度 `1..10^5`，英文字母），返回 `s` 中包含 `t` 全部字符（含重复次数）的最短子串，不存在返回空串。

```python
from collections import Counter
def min_window(s: str, t: str) -> str:
    need = Counter(t)
    missing = len(t)
    left = start = end = 0
    for right, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if end == 0 or right - left < end - start:
                start, end = left, right
    return s[start:end]
```

**例题：** LC 1004 最大连续1的个数 III

二进制数组 `nums`（`1 <= length <= 10^5`）最多可把 `k` 个 0 翻成 1，求翻转后连续 1 的最大个数。

```python
def longest_ones(nums: list[int], k: int) -> int:
    best = left = zeros = 0                # 窗口 nums[left : right + 1]，zeros 是窗口内 0 的个数
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:                   # 0 太多：缩左端直到窗口合法
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

**例题：** LC 560 和为 K 的子数组

整数数组 `nums`（`1 <= length <= 2 * 10^4`，`-1000 <= v <= 1000`，含负数）和整数 `k`，统计和为 `k` 的连续子数组个数。

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

**例题：** LC 300 最长递增子序列

整数数组 `nums`（`1 <= length <= 2500`），求最长严格递增子序列的长度（子序列不要求连续）。

```python
from bisect import bisect_left
def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []                          # tails[k] = 长度为 k+1 的递增子序列的最小结尾
    for x in nums:
        i = bisect_left(tails, x)                  # 严格递增：第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)                        # x 比所有结尾都大：最长长度 +1
        else:
            tails[i] = x                           # 让长度 i+1 的结尾变得更小，对后面更有利
    return len(tails)
```

**例题：** LC 1248 统计「优美子数组」

整数数组 `nums`（`1 <= length <= 50000`）和 `k`，统计恰好含 `k` 个奇数的连续子数组个数。

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

**例题：** LC 239 滑动窗口最大值

整数数组 `nums`（`1 <= length <= 10^5`）和窗口大小 `k`，窗口每次右移一位，返回每个窗口内的最大值。

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

**例题：** LC 395 至少有 K 个重复字符的最长子串

字符串 `s`（`1 <= length <= 10^4`，小写字母）和 `k`（`1 <= k <= 10^5`），求最长子串，要求其中每个字符出现次数都不少于 `k`，没有则为 `0`。

```python
from collections import Counter
def longest_substring(s: str, k: int) -> int:
    if len(s) < k:
        return 0
    count = Counter(s)
    bad = next((ch for ch, c in count.items() if c < k), None)   # 任意一个出现次数不足 k 的字符
    if bad is None:
        return len(s)                          # 整串已经合法
    return max(longest_substring(part, k) for part in s.split(bad))   # 含 bad 的子串一定不合法，按它切开
```

**例题：** LC 438 找到字符串中所有字母异位词

字符串 `s` 和 `p`，返回 `s` 中所有是 `p` 的异位词的子串起始下标；`1 <= s.length, p.length <= 3 * 10^4`，只含小写字母。

```python
from collections import Counter
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
