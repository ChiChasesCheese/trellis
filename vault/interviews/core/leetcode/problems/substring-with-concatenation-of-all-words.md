---
slug: substring-with-concatenation-of-all-words
---
## Q
**LC 30 串联所有单词的子串**｜Hard

`words` 里的单词长度相同。返回 `s` 中所有恰好由全部单词按任意顺序首尾相接而成的子串的起始下标（重复单词按次数用）。

## A
**一句话。** 把单词当「大字母」做定长滑动窗口：对每个起点余数 `0..w-1` 各扫一遍，用 `Counter` 记窗口内单词个数。

```python
def find_substring(s, words):
    w, k, n = len(words[0]), len(words), len(s)
    need = Counter(words)
    ans = []
    for off in range(w):               # 起点按余数分 w 组
        have, left = Counter(), off
        for r in range(off, n - w + 1, w):
            word = s[r:r + w]
            if word not in need:
                have.clear()           # 窗口作废
                left = r + w
                continue
            have[word] += 1
            while have[word] > need[word]:
                have[s[left:left + w]] -= 1   # 吐出左端
                left += w
            if r + w - left == k * w:
                ans.append(left)
                have[s[left:left + w]] -= 1
                left += w
    return ans
```

**复杂度。** 时间 `O(n·w)`，空间 `O(k·w)`。

**易错点。**
- 只扫偏移 `0`：`s="xfoobar"`、`words=["foo","bar"]` 得 `[]`，应为 `[1]`。
- 只判单词是否出现、不计次数：`s="foofoo"`、`words=["foo","bar"]` 得 `[0]`，应为 `[]`。
- 遇到不在 `words` 里的单词没清空窗口：旧计数带进下一段。

**追问。**
- 单词长度不一样？：定长切分失效，改用 Trie 或 Aho-Corasick 加回溯或 DP。
- 怎么省掉重复的字符串哈希？：先把每个位置的单词映射成整数编号，再在整数上滑窗。

**同模式。** LC 76 最小覆盖子串、LC 438 找到字符串中所有字母异位词、LC 567 字符串的排列、LC 3 无重复字符的最长子串
