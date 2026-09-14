---
id: leetcode-c-endlesscheng-9ozfk9-largest-rectangle-histogram-template
node: stack-queue-monotonic.largest-rectangle-histogram
type: cloze
anki: 1787272403403
tags: [concept-cloze, leetcode, recall, template]
---
直方图最大矩形常在高度数组两端加入 {{c1::0 哨兵}}，以统一结算。

```
def largest_rectangle_area(heights: list[int]) -> int:
    values = [0] + heights + [0]
    stack = [0]
    best = 0
    for i in range(1, len(values)):
        while values[stack[-1]] > values[i]:
            mid = stack.pop()
            width = i - stack[-1] - 1
            best = max(best, values[mid] * width)
        stack.append(i)
    return best
```

**Evidence**

二、矩形

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.02%20-%20%E7%9B%B4%E6%96%B9%E5%9B%BE%E6%9C%80%E5%A4%A7%E7%9F%A9%E5%BD%A2)
