---
id: leetcode-c-endlesscheng-sjfwqi-subsequence-automaton-template
node: strings.subsequence-automaton
type: cloze
anki: 1787272449979
tags: [concept-cloze, leetcode, recall, template]
---
匹配到下标 found 后，下一状态必须更新为 {{c1::found + 1}}，以保证子序列下标递增。

```
def build_subsequence_automaton(text):
    n = len(text)
    next_pos = [[-1] * 26 for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        next_pos[i] = next_pos[i + 1].copy()
        next_pos[i][ord(text[i]) - ord('a')] = i
    return next_pos

def is_subsequence(pattern, next_pos):
    pos = 0
    n = len(next_pos) - 1
    for ch in pattern:
        if pos > n:
            return False
        found = next_pos[pos][ord(ch) - ord('a')]
        if found == -1:
            return False
        pos = found + 1
    return True
```

**Evidence**

九、子序列自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.10%20-%20%E5%AD%90%E5%BA%8F%E5%88%97%E8%87%AA%E5%8A%A8%E6%9C%BA)
