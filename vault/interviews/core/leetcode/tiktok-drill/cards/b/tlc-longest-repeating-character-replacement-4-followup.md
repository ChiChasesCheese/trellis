---
id: tlc-longest-repeating-character-replacement-4-followup
node: b.longest-repeating-character-replacement
type: qa
step: 4
---
## Q
**LC 424 替换后的最长重复字符**｜追问

面试官接着问：（1）如果不想用「过期的 `max_freq`」这个技巧，怎么写才显然正确？（2）要返回具体的子串？（3）只有 `0/1` 数组，最多翻转 `k` 个 `0`（LC 1004）？

## A
1. **每次重算最大频次**：用 `while` 收缩，并在判断条件里直接取 `max(count.values())`，显然正确，代价是常数乘以字符集大小。
```python
from collections import Counter

def character_replacement_safe(s: str, k: int) -> int:
    count: Counter[str] = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while right - left + 1 - max(count.values()) > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```
结果与主解法相同（`"AABABBA", k = 1` → `4`），时间 `O(26n)`。
2. **返回子串**：主解法只保证最终的窗口**长度**正确，窗口内容可能并不合法（`max_freq` 是过期值）。要子串就用上面的安全写法，在更新 `best` 时记录 `left`，返回 `s[start : start + best]`。
3. **0/1 数组翻转 0**：把「替换代价」换成窗口内 `0` 的个数：`zeros > k` 就收缩。
```python
def longest_ones(nums: list[int], k: int) -> int:
    left = zeros = 0
    for right, x in enumerate(nums):
        zeros += x == 0
        if zeros > k:
            zeros -= nums[left] == 0
            left += 1
    return len(nums) - left
```
`longest_ones([1,1,1,0,0,0,1,1,1,1,0], 2)` → `6`。

**Python 提醒**：`zeros += x == 0` 利用布尔是整数的子类，`True` 当 `1` 加；读代码的人容易困惑时，写成 `if x == 0: zeros += 1`。
