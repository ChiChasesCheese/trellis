---
id: leetcode-c-endlesscheng-g6ktkl-wildcard-parentheses-range-template
node: greedy-sorting.wildcard-parentheses-range
type: cloze
anki: 1787272435206
tags: [concept-cloze, leetcode, recall, template]
---
每轮更新后执行 {{c1::low = max(low, 0)}}。

```
def valid_parentheses(s: str) -> bool:
    low = high = 0
    for ch in s:
        if ch == '(':
            low += 1
            high += 1
        elif ch == ')':
            low -= 1
            high -= 1
        else:
            low -= 1
            high += 1
        if high < 0:
            return False
        low = max(low, 0)
    return low == 0
```

**Evidence**

§3.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.13%20-%20%E9%80%9A%E9%85%8D%E5%90%88%E6%B3%95%E6%8B%AC%E5%8F%B7%E8%8C%83%E5%9B%B4%E8%B4%AA%E5%BF%83)
