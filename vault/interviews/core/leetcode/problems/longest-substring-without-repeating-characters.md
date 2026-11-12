---
slug: longest-substring-without-repeating-characters
---
## Q
**LC 3 无重复字符的最长子串**｜Medium

给字符串 `s`，求不含重复字符的最长子串（连续）的长度。

## A
**一句话。** 可变长滑动窗口：撞上窗口内的重复字符时，左端直接跳到它上次出现位置的下一位。

```python
def length_of_longest_substring(s):
    last = {}                      # 字符 -> 最近出现的下标
    best = left = 0                # 窗口是 s[left:right+1]
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:   # 在窗口内出现过
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(min(n, Σ))`。

**易错点。**
- 只写 `ch in last`：字典里有已滑出窗口的旧位置，会让左端后退。`"abba"` 得 `3`，应为 `2`。
- 最后一个窗口漏记：`best` 要在循环里每步更新，不能只在撞重复时更新。

**追问。**
- 要返回子串本身？：更新答案时一并记起点 `start = left`。
- 每个字符至多出现 `k` 次？：改用 `Counter`，违规时 `while` 缩左端（扩右、缩左、更新三步）。

**同模式。** LC 340 至多包含 K 个不同字符的最长子串、LC 424 替换后的最长重复字符、LC 76 最小覆盖子串
