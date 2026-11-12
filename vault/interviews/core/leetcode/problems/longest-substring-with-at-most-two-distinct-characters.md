---
slug: longest-substring-with-at-most-two-distinct-characters
---
## Q
**LC 159 至多包含两个不同字符的最长子串**｜Medium

求字符串 `s` 中至多含两种不同字符的最长子串的长度。

## A
**一句话。** 滑动窗口维护「种类数不超过 2」，超标就从左端吐字符。

```python
def length_of_longest_substring_two_distinct(s):
    count = defaultdict(int)   # 窗口内每个字符的次数
    best = left = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > 2:  # 种类超标，吐左端
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]   # 归零必须删键
            left += 1
        best = max(best, right - left + 1)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 次数归零不删键：`len(count)` 不回落，`"eceba"` 得 `2`，应为 `3`。
- `while` 写成 `if`：一次只吐一个，窗口里可能还留着 3 种。
- 收缩前就更新 `best`：把非法窗口的长度记进答案。

**追问。**
- 要输出这个子串？：记下取最大时的 `left`，返回 `s[start:start+best]`。
- 输入是字符流不能回看？：字典只存 2 个字符的最后下标，空间 `O(1)`。

**同模式。** LC 3 无重复字符的最长子串、LC 340 至多包含 K 个不同字符的最长子串、LC 904 水果成篮、LC 424 替换后的最长重复字符
