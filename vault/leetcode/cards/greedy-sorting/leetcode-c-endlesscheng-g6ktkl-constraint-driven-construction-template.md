---
id: leetcode-c-endlesscheng-g6ktkl-constraint-driven-construction-template
node: greedy-sorting.constraint-driven-construction
type: cloze
anki: 1787272438507
tags: [concept-cloze, leetcode, recall, template]
---
交替构造两类字符前，先检查频次差是否 {{c1::不超过 1}}。

```
def build_alternating(count_a: int, count_b: int) -> str:
    if abs(count_a - count_b) > 1:
        return ''
    first, second = ('a', 'b') if count_a >= count_b else ('b', 'a')
    result = []
    while count_a or count_b:
        if first == 'a' and count_a:
            result.append('a')
            count_a -= 1
        elif first == 'b' and count_b:
            result.append('b')
            count_b -= 1
        first, second = second, first
    return ''.join(result)
```

**Evidence**

六、构造题

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.24%20-%20%E7%BA%A6%E6%9D%9F%E9%A9%B1%E5%8A%A8%E6%9E%84%E9%80%A0)
