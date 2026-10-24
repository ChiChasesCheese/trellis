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
**固定窗口**：先装满 `m - 1` 个，之后每步「进一个、出一个」。

```python
from collections import Counter
def find_anagrams(s: str, p: str) -> list[int]:
    m = len(p)
    need, window = Counter(p), Counter(s[:m - 1])
    res: list[int] = []
    for i in range(m - 1, len(s)):
        window[s[i]] += 1                  # 右端进
        if window == need:                 # 3.10+ 的 Counter 相等判断忽略计数为 0 的键
            res.append(i - m + 1)
        window[s[i - m + 1]] -= 1          # 左端出
    return res
print(find_anagrams("cbaebabacd", "abc"), find_anagrams("abab", "ab"))   # [0, 6] [0, 1, 2]
```

LC 1151 把所有 1 聚到一起：窗口长度 `k = sum(data)`，最少交换 = `k` 减去任意窗口里 1 的最大个数；环形版（LC 2134）把数组拼上自己的前 `k-1` 个元素。

**恰好 `k` = 至多 `k` − 至多 `k-1`**（LC 1248）：「至多」满足单调性，可用窗口；以 `right` 结尾的合法子数组有 `right - left + 1` 个。

```python
def at_most_odd(nums: list[int], k: int) -> int:
    if k < 0:
        return 0
    left = odd = res = 0
    for right, x in enumerate(nums):
        odd += x & 1
        while odd > k:
            odd -= nums[left] & 1
            left += 1
        res += right - left + 1            # 以 right 结尾的合法子数组个数
    return res
print(at_most_odd([1,1,2,1,1], 3) - at_most_odd([1,1,2,1,1], 2))   # 2
```

**LC 424 非收缩窗口**：窗口只会变长或平移，`max_cnt`（历史最大频次）只增不减，窗口长度最终就是答案；`max_cnt` 过时不影响正确性，因为只有 `max_cnt` 变大才可能让窗口变长。
