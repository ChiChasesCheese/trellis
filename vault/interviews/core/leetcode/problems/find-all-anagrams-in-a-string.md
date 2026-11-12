---
slug: find-all-anagrams-in-a-string
---
## Q
**LC 438 找到字符串中所有字母异位词**｜Medium

返回 `s` 中所有是 `p` 的异位词的子串的起始下标。

## A
**一句话。** 定长滑动窗口：计数表记录窗口还缺哪些字母，维护「计数非 0 的字母种数」，为 `0` 即异位词。

```python
def find_anagrams(s, p):
    m = len(p)
    need = Counter(p)    # 窗口还缺几个；负数表示多了
    bad = len(need)      # need[c] != 0 的字母种数
    ans = []

    def shift(c, d):     # 窗口增减一个 c，返回 bad 的变化
        was = need[c] != 0
        need[c] += d
        return (need[c] != 0) - was

    for r, ch in enumerate(s):
        bad += shift(ch, -1)              # 右端进
        if r >= m:
            bad += shift(s[r - m], +1)    # 左端出
        if bad == 0:
            ans.append(r - m + 1)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(26)`。

**易错点。**
- 只比较字母集合：`s="aab"`、`p="abb"` 集合相同，会返回 `[0]`，应为 `[]`。
- 左端出窗口的时机：要等 `r >= m` 窗口满了再踢 `s[r-m]`，早踢晚踢都错。
- 起始下标写成 `r`：`"abab"`、`"ab"` 得 `[1,2,3]`，应为 `[0,1,2]`。

**追问。**
- 只问是否存在（LC 567）？：第一次 `bad == 0` 就返回 `True`。
- 同时匹配很多个 `p`？：每个 `p` 扫一遍是 `O(nk)`；一次扫描可用 Aho–Corasick 或计数向量哈希。

**同模式。** LC 567 字符串的排列、LC 76 最小覆盖子串、LC 242 有效的字母异位词、LC 30 串联所有单词的子串
