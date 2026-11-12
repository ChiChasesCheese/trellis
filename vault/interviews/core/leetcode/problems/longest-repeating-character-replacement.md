---
slug: longest-repeating-character-replacement
---
## Q
**LC 424 替换后的最长重复字符**｜Medium

大写字母串 `s` 最多可替换 `k` 个字符，求替换后全是同一字母的最长子串的长度。

## A
**一句话。** 滑动窗口：窗口长度减最高频字符数 `<= k` 才合法，超了就整体右移一格而不缩小。

```python
def character_replacement(s, k):
    count = Counter()
    max_freq = left = 0           # max_freq 只增不减
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        if right - left + 1 - max_freq > k:   # 要换的太多
            count[s[left]] -= 1
            left += 1
    return len(s) - left          # 窗口只增或平移
```

**复杂度。** 时间 `O(n)`，空间 `O(26)`。

**易错点。**
- 判断写成 `>= k`：少一个替换名额，`"ABAB"`、`k=2` 得 `3`，应为 `4`。
- 把 `if` 写成 `while` 并重算 `max_freq`：也对，但变成 `O(26n)`。

**追问。**
- `max_freq` 过期了为什么没事？：窗口只有在频次真创新高时才变长，过期的偏大值最多让窗口平移，答案不会虚高。
- 0/1 数组最多翻 `k` 个 0？：窗口内 0 的个数 `> k` 就缩，同一个框架（LC 1004）。

**同模式。** LC 1004 最大连续1的个数 III、LC 2024 考试的最大困扰度、LC 3 无重复字符的最长子串、LC 340 至多包含 K 个不同字符的最长子串
