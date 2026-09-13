---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-lexicographically-smallest-subsequence-template
node: stack-queue-monotonic.monotonic-stack-lexicographic-subsequence
type: cloze
anki: 1787272404006
tags: [concept-cloze, leetcode, recall, template]
---
最小去重子序列模板需要同时维护 {{c1::remaining 计数}} 和 {{c2::in_stack 集合}}。

```
def smallest_unique_subsequence(text: str) -> str:
    remaining: dict[str, int] = {}
    for ch in text:
        remaining[ch] = remaining.get(ch, 0) + 1
    stack: list[str] = []
    in_stack: set[str] = set()
    for ch in text:
        remaining[ch] -= 1
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and remaining[stack[-1]] > 0:
            in_stack.remove(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return ''.join(stack)
```

**Evidence**

四、最小字典序

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.04%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E6%9E%84%E9%80%A0%E6%9C%80%E5%B0%8F%E5%AD%97%E5%85%B8%E5%BA%8F%E5%AD%90%E5%BA%8F%E5%88%97)
