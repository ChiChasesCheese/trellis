---
id: tlc-longest-substring-without-repeating-characters-2-code
node: p1.longest-substring-without-repeating-characters
type: qa
step: 2
---
## Q
**LC 3 无重复字符的最长子串**｜写出 Python 实现

字符串 `s`（长度至多 `10^5`）里不含重复字符的最长连续子串有多长？要求 `O(n)`。

## A
**思路。** 右端逐个前进；字典 `last` 记每个字符最近一次出现的下标。新字符如果在**当前窗口内**出现过，左端直接跳到它上次位置的下一位；每步用窗口长度更新答案。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}          # 字符 -> 它最近一次出现的下标
    best = left = 0                    # 窗口是 s[left : right + 1]
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:   # ch 在窗口内出现过：左端直接跳过去
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

运行：`"abcabcbb"` → `3`，`"bbbbb"` → `1`，`"pwwkew"` → `3`，`""` → `0`，`"abba"` → `2`。

**复杂度。** 时间 `O(n)`：右端走 `n` 步，每步字典操作 `O(1)`；空间 `O(min(n, Σ))`，`Σ` 是字符集大小（ASCII 时最多 128）。

**写法要点。** `enumerate` 同时拿下标和字符；`last.get(ch, -1)` 一次完成「是否出现过」和「在哪」，不用先 `in` 再取值；`best = left = 0` 链式赋值只适合不可变值。
