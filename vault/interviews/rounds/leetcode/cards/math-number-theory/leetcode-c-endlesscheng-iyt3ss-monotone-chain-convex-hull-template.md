---
id: leetcode-c-endlesscheng-iyt3ss-monotone-chain-convex-hull-template
node: math-number-theory.monotone-chain-convex-hull
type: cloze
anki: 1787272428908
tags: [concept-cloze, leetcode, recall, template]
---
标准不保留共线边中间点的条件是 cross(...) {{c1::<= 0}}。

```
def convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]
```

**Evidence**

§5.4 凸包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.14%20-%20Andrew%20%E5%8D%95%E8%B0%83%E9%93%BE%E5%87%B8%E5%8C%85)
