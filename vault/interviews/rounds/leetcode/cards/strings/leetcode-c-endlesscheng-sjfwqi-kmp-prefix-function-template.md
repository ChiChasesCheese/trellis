---
id: leetcode-c-endlesscheng-sjfwqi-kmp-prefix-function-template
node: strings.kmp-prefix-function
type: cloze
anki: 1787272447505
tags: [concept-cloze, leetcode, recall, template]
---
KMP 找到一次完整匹配后，应执行 {{c1::j = pi[j - 1]}}，以保留可能的重叠匹配。

```
def kmp_search(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))
    pi = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    ans = []
    j = 0
    for i, ch in enumerate(text):
        while j and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            ans.append(i - len(pattern) + 1)
            j = pi[j - 1]
    return ans
```

**Evidence**

一、KMP（前缀的后缀）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.01%20-%20KMP%20%E7%AE%97%E6%B3%95%EF%BC%88%E5%89%8D%E7%BC%80%E5%87%BD%E6%95%B0%20-%20border%EF%BC%89)
