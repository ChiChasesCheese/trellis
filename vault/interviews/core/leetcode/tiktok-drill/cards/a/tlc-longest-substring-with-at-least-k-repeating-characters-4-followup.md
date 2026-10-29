---
id: tlc-longest-substring-with-at-least-k-repeating-characters-4-followup
node: a.longest-substring-with-at-least-k-repeating-characters
type: qa
step: 4
---
## Q
**LC 395 至少有 K 个重复字符的最长子串**｜追问

面试官接着问：（1）不用递归，用滑动窗口怎么做？（2）字符集不止 26 个会怎样？（3）要返回子串本身？

## A
1. **枚举种数的滑窗**：固定窗口内最多 `target` 种字符，这时「种数超了就收缩」是单调的；`enough` 记录次数已达 `k` 的种数，`unique == enough == target` 时窗口合法。
```python
from collections import Counter

def longest_substring_window(s: str, k: int) -> int:
    best = 0
    for target in range(1, len(set(s)) + 1):   # 枚举窗口内允许的不同字符种数
        count: Counter[str] = Counter()
        left = unique = enough = 0             # enough：出现次数已达 k 的字符种数
        for right, ch in enumerate(s):
            count[ch] += 1
            if count[ch] == 1:
                unique += 1
            if count[ch] == k:
                enough += 1
            while unique > target:             # 种数超了，收缩左端
                out = s[left]
                if count[out] == k:
                    enough -= 1
                count[out] -= 1
                if count[out] == 0:
                    unique -= 1
                left += 1
            if unique == enough == target:
                best = max(best, right - left + 1)
    return best
```
`("aaabb", 3)` → `3`，`("ababbc", 2)` → `5`，`("aaacbbb", 3)` → `3`。时间 `O(26n)`，空间 `O(26)`。
2. **字符集很大**：分治的深度最多等于不同字符数，最坏 `O(n · σ)`（`σ` 是字符种数），可能到 `O(n^2)`；滑窗要枚举 `σ` 轮，同样变慢。需要换成基于排序次数的结构，通常不是面试要求。
3. **返回子串**：递归返回 `(长度, 起点)`，切分时把每段的起点偏移加回去；滑窗版在更新 `best` 时记 `right - best + 1`。

**Python 提醒**：`Counter` 的值减到 `0` 后键仍在；统计「种数」要自己维护 `unique`，不要用 `len(count)`，除非减到 `0` 时 `del count[ch]`。
