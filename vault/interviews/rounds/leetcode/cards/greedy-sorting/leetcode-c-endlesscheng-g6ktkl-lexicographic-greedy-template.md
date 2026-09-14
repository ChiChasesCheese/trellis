---
id: leetcode-c-endlesscheng-g6ktkl-lexicographic-greedy-template
node: greedy-sorting.lexicographic-greedy
type: cloze
anki: 1787272434606
tags: [concept-cloze, leetcode, recall, template]
---
最小子序列单调栈中，栈顶大于当前字符且仍可删除时应 {{c1::弹栈}}。

```
def smallest_subsequence(s: str, k: int) -> str:
    stack: list[str] = []
    remove = len(s) - k
    for ch in s:
        while remove and stack and stack[-1] > ch:
            stack.pop()
            remove -= 1
        stack.append(ch)
    return ''.join(stack[:k])
```

**Evidence**

§3.1

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.11%20-%20%E5%AD%97%E5%85%B8%E5%BA%8F%E8%B4%AA%E5%BF%83)
