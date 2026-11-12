---
slug: minimum-window-substring
---
## Q
**LC 76 最小覆盖子串**｜Hard

给字符串 `s` 和 `t`，返回 `s` 中最短的、包含 `t` 全部字符（含重复次数）的子串，不存在返回 `""`。

## A
**一句话。** 滑动窗口加计数表：右端吞字符，覆盖后收缩左端取最短，再丢一个必需字符继续。

```python
def min_window(s, t):
    need = Counter(t)     # >0 还缺，<0 窗口里多出来
    missing = len(t)      # 还缺的字符总数（含重复）
    best_l, best_len = 0, len(s) + 1
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:                 # 已覆盖，尽量收缩
            while need[s[left]] < 0:     # 左端多余，丢掉
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_l, best_len = left, right - left + 1
            need[s[left]] += 1           # 丢一个必需字符
            missing += 1
            left += 1
    if best_len > len(s):
        return ""
    return s[best_l:best_l + best_len]
```

**复杂度。** 时间 `O(m+n)`，空间 `O(Σ)`。

**易错点。**
- 用集合代替计数：`s="a", t="aa"` 会返回 `"a"`，应为 `""`。
- 收缩条件写成 `> 0` 或 `!= 0`：「多余」必须是 `need[s[left]] < 0`。
- 先丢必需字符再记答案：会漏掉当前窗口。

**追问。**
- `t` 很短而 `s` 很长？：先过滤出 `s` 中属于 `t` 的字符及下标，只在这些位置上滑动。
- `t` 要按顺序出现（LC 727）？：不能用计数，改用正向匹配再反向收缩，或动态规划。

**同模式。** LC 3 无重复字符的最长子串、LC 438 找到字符串中所有字母异位词、LC 567 字符串的排列、LC 727 最小窗口子序列
