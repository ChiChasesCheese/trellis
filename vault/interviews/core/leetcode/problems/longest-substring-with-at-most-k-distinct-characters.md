---
slug: longest-substring-with-at-most-k-distinct-characters
---
## Q
**LC 340 至多包含 K 个不同字符的最长子串**｜Medium

给字符串 `s` 和整数 `k`，求至多含 `k` 种不同字符的最长子串的长度。

## A
**一句话。** 滑动窗口加计数器：种类数超过 `k` 就缩左端，计数归零要删键。

```python
def length_of_longest_substring_k_distinct(s, k):
    count = Counter()             # 窗口内每个字符的次数
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:     # 种类超了：缩左端
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]    # 删键，len 才准
            left += 1
        best = max(best, right - left + 1)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(k)`。

**易错点。**
- 计数归零不删键：`len(count)` 把已出窗的字符也算上，`"eceba"`、`k=2` 时 `left` 越界抛 `IndexError`。
- 把 `best` 更新放在 `while` 之前：窗口此时不合法，会多算。

**追问。**
- `k = 0` 要特判吗？：不用，窗口缩成空，`best` 一直是 `0`。
- 要「恰好 `k` 种」？：`atMost(k) - atMost(k-1)`，见 LC 992。

**同模式。** LC 3 无重复字符的最长子串、LC 159 至多包含两个不同字符的最长子串、LC 904 水果成篮、LC 992 K 个不同整数的子数组
