---
id: leetcode-c-endlesscheng-iyt3ss-computational-geometry-primitives-template
node: math-number-theory.computational-geometry-primitives
type: cloze
anki: 1787272428605
tags: [concept-cloze, leetcode, recall, template]
---
整数坐标下比较两段距离时，优先比较 {{c1::平方距离}}。

```
def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def squared_distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

def polygon_area2(points):
    return sum(points[i][0] * points[(i + 1) % len(points)][1] - points[i][1] * points[(i + 1) % len(points)][0] for i in range(len(points)))
```

**Evidence**

§5.1 点、线；§5.2 圆

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.13%20-%20%E8%AE%A1%E7%AE%97%E5%87%A0%E4%BD%95%E5%9F%BA%E6%9C%AC%E8%B0%93%E8%AF%8D)
