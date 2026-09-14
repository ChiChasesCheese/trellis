---
id: leetcode-c-endlesscheng-g6ktkl-reverse-thinking-template
node: fundamentals.reverse-thinking
type: cloze
anki: 1787272437307
tags: [concept-cloze, leetcode, recall, template]
---
单位代价逆向搜索可从 target 开始用 {{c1::deque BFS}}。

```
from collections import deque

def min_steps_reverse(start: int, target: int) -> int:
    queue = deque([(target, 0)])
    seen = {target}
    while queue:
        value, steps = queue.popleft()
        if value == start:
            return steps
        for previous in (value - 1, value // 2 if value % 2 == 0 else -1):
            if previous >= 0 and previous not in seen:
                seen.add(previous)
                queue.append((previous, steps + 1))
    return -1
```

**Evidence**

§5.4

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.20%20-%20%E9%80%86%E5%90%91%E6%80%9D%E7%BB%B4)
