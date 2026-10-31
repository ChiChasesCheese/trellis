---
id: tlc-patterns-sliding-window-5-variants
node: patterns.sliding-window
type: qa
step: 5
---
## Q
**滑动窗口（Sliding Window）｜变形：固定窗口、至多 k 与恰好 k、非收缩窗口**

固定长度窗口怎么写？「恰好 `k`」怎样转成「至多 `k`」？LC 424 的窗口为什么可以不缩小？

## A
- **固定窗口（比较计数）**：先装满再每步「进一个、出一个」；用计数表记录窗口与目标的差，差全为 0 时窗口就是一个字母异位词（例：LC 438 找到字符串中所有字母异位词）。
- **固定窗口（求窗口内的和）**：窗口长度由数据决定，把 1 聚在一起的窗口长度是 `sum(data)`，最少交换次数 = 窗口长度减去任意窗口里 1 的最大个数；环形版（LC 2134）把数组拼上自己的前 `w - 1` 个元素（例：LC 1151 最少交换次数来组合所有的 1）。
- **恰好 `k` = 至多 `k` − 至多 `k-1`**：「至多」满足单调性，可用窗口，以 `right` 结尾的合法子数组有 `right - left + 1` 个；折叠里的解把这个差分写成「前缀里奇数个数为 `odd - k` 的位置有几个」，和前缀和是同一个思路（例：LC 1248 统计「优美子数组」）。
- **非收缩窗口**：窗口只会变长或平移，`max_freq`（历史最大频次）只增不减，窗口长度最终就是答案；`max_freq` 过时不影响正确性，因为只有 `max_freq` 变大才可能让窗口变长（例：LC 424 替换后的最长重复字符）。

**例题：** LC 438 找到字符串中所有字母异位词

返回 `s` 中所有 `p` 的字母异位词子串的起始下标，`1 <= s.length, p.length <= 3 * 10^4`，仅小写字母。

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

**例题：** LC 1151 最少交换次数来组合所有的 1

二进制数组 `data`，通过交换位置把所有 1 组合到一起，返回最少交换次数，`1 <= data.length <= 10^5`。

```python
def min_swaps(data: list[int]) -> int:
    w = sum(data)
    cur = sum(data[:w])
    best = cur
    for i in range(w, len(data)):
        cur += data[i] - data[i - w]
        best = max(best, cur)
    return w - best
```

**例题：** LC 1248 统计「优美子数组」

统计恰好有 `k` 个奇数的连续子数组个数，`1 <= nums.length <= 50000`，`1 <= nums[i] <= 10^5`。

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

**例题：** LC 424 替换后的最长重复字符

最多把 `k` 个字符改成任意大写字母，求之后包含相同字母的最长子串长度，`1 <= s.length <= 10^5`，仅大写字母。

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
