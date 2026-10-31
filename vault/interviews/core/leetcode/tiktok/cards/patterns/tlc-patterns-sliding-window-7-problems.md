---
id: tlc-patterns-sliding-window-7-problems
node: patterns.sliding-window
type: qa
step: 7
---
## Q
**滑动窗口（Sliding Window）｜本组用到滑动窗口的题**

按变形分类，这个题组里哪些题的核心是滑动窗口？

## A
**最长（违反约束才缩）**
- LC 3 无重复字符的最长子串
- LC 340 至多包含 K 个不同字符的最长子串
- LC 904 水果成篮（`k = 2` 的 LC 340）
- LC 424 替换后的最长重复字符
- LC 845 数组中的最长山脉（可用窗口 / 双指针）
- LC 1004 最大连续1的个数 III（高频）

**最短（满足约束就缩）**
- LC 209 长度最小的子数组
- LC 76 最小覆盖子串

**固定窗口**
- LC 438 找到字符串中所有字母异位词

**至多 `k` 与恰好 `k`**
- LC 1248 统计「优美子数组」

**窗口 + 其他结构**
- LC 239 滑动窗口最大值（单调队列）
- LC 395 至少有 K 个重复字符的最长子串（约束不单调，枚举种类数）

提示：先判断**最长还是最短**决定更新位置；再判断约束是否单调，不单调就换前缀和或枚举。

**例题：** LC 3 无重复字符的最长子串

字符串 `s`，求不含重复字符的最长子串的长度；`0 <= s.length <= 10^5`。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}
    best = left = 0
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**例题：** LC 340 至多包含 K 个不同字符的最长子串

字符串 `s` 和整数 `k`，求至多含 `k` 个不同字符的最长子串的长度；`s.length <= 5 * 10^4`，`0 <= k <= 50`。

```python
from collections import Counter
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    count: Counter[str] = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]
            left += 1
        best = max(best, right - left + 1)
    return best
```

**例题：** LC 904 水果成篮

`fruits[i]` 是第 `i` 棵树的水果种类，两个篮子各装一种，从任一棵树起只能向右连续采摘，求最多摘几个；`fruits.length <= 10^5`。

```python
from collections import Counter
def total_fruit(fruits: list[int]) -> int:
    count: Counter[int] = Counter()
    best = left = 0
    for right, kind in enumerate(fruits):
        count[kind] += 1
        while len(count) > 2:
            gone = fruits[left]
            count[gone] -= 1
            if count[gone] == 0:
                del count[gone]
            left += 1
        best = max(best, right - left + 1)
    return best
```

**例题：** LC 424 替换后的最长重复字符

大写字符串 `s`，最多把 `k` 个字符改成任意字母，求能得到的最长相同字母子串的长度；`s.length <= 10^5`，`0 <= k <= s.length`。

```python
from collections import Counter
def character_replacement(s: str, k: int) -> int:
    count: Counter[str] = Counter()
    max_freq = left = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        if right - left + 1 - max_freq > k:
            count[s[left]] -= 1
            left += 1
    return len(s) - left
```

**例题：** LC 845 数组中的最长山脉

山脉是长度不小于 `3`、先严格上升再严格下降的连续子数组，求 `arr` 中最长山脉的长度，没有返回 `0`；`arr.length <= 10^4`。

```python
def longest_mountain(arr: list[int]) -> int:
    n = len(arr)
    best = 0
    i = 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:
            left = i - 1
            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1
            right = i + 1
            while right < n - 1 and arr[right] > arr[right + 1]:
                right += 1
            best = max(best, right - left + 1)
            i = right
        else:
            i += 1
    return best
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

**例题：** LC 76 最小覆盖子串

字符串 `s` 和 `t`，求 `s` 中包含 `t` 全部字符（含重复次数）的最短子串，没有返回 `""`；`s.length, t.length <= 10^5`。

```python
from collections import Counter
def min_window(s: str, t: str) -> str:
    need = Counter(t)
    missing = len(t)
    best_l, best_len = 0, len(s) + 1
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_l, best_len = left, right - left + 1
            need[s[left]] += 1
            missing += 1
            left += 1
    return "" if best_len > len(s) else s[best_l : best_l + best_len]
```

**例题：** LC 438 找到字符串中所有字母异位词

字符串 `s` 和 `p`，返回 `s` 中所有 `p` 的异位词子串的起始下标；`s.length, p.length <= 3 * 10^4`，小写字母。

```python
from collections import Counter
def find_anagrams(s: str, p: str) -> list[int]:
    m = len(p)
    need = Counter(p)
    unbalanced = len(need)
    ans: list[int] = []
    def shift(c: str, d: int) -> int:
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

**例题：** LC 1248 统计「优美子数组」

整数数组 `nums` 和 `k`，统计恰好含 `k` 个奇数的连续子数组个数；`nums.length <= 50000`，`1 <= k <= nums.length`。

```python
def number_of_subarrays(nums: list[int], k: int) -> int:
    seen = [0] * (len(nums) + 1)
    seen[0] = 1
    odd = ans = 0
    for x in nums:
        odd += x & 1
        if odd >= k:
            ans += seen[odd - k]
        seen[odd] += 1
    return ans
```

**例题：** LC 239 滑动窗口最大值

大小为 `k` 的窗口从左到右滑过 `nums`，返回每个窗口的最大值；`nums.length <= 10^5`，`1 <= k <= nums.length`。

```python
from collections import deque
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    window: deque[int] = deque()
    ans: list[int] = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.popleft()
        if i >= k - 1:
            ans.append(nums[window[0]])
    return ans
```

**例题：** LC 395 至少有 K 个重复字符的最长子串

小写字符串 `s` 和 `k`，求最长子串，使其中每个字符出现次数都不少于 `k`，返回长度；`s.length <= 10^4`。

```python
from collections import Counter
def longest_substring(s: str, k: int) -> int:
    if len(s) < k:
        return 0
    count = Counter(s)
    bad = next((ch for ch, c in count.items() if c < k), None)
    if bad is None:
        return len(s)
    return max(longest_substring(part, k) for part in s.split(bad))
```

**例题：** LC 1004 最大连续1的个数 III

给一个二进制数组 `nums` 和整数 `k`，最多可以把 `k` 个 `0` 翻成 `1`，求操作后**连续 `1` 的最大个数**。`1 <= nums.length <= 10^5`，`nums[i]` 只能是 `0` 或 `1`，`0 <= k <= nums.length`。

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
