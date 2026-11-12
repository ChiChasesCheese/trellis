---
slug: first-unique-character-in-a-string
---
## Q
**LC 387 字符串中的第一个唯一字符**｜Easy

返回字符串 `s` 中第一个不重复字符的下标，不存在返回 `-1`。

## A
**一句话。** 第一遍计数，第二遍按原顺序找第一个次数为 `1` 的字符。

```python
def first_uniq_char(s):
    cnt = Counter(s)
    for i, ch in enumerate(s):
        if cnt[ch] == 1:
            return i
    return -1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（26 个字母）。

**易错点。**
- 返回字符而不是下标：`"leetcode"` 应返回 `0`。
- 边扫边判断：`"aabc"` 在第一个 `a` 就误返回 `0`，必须等整串统计完。

**追问。**
- 字符流式到来怎么办？：用 `OrderedDict` 或队列，惰性弹出队首已重复的字符。

**同模式。** LC 383 赎金信、LC 242 有效的字母异位词、LC 409 最长回文串、LC 451 根据字符出现频率排序
