---
id: leetcode-c-endlesscheng-mor1u6-two-dimensional-prefix-and-difference-template
node: arrays-hash-prefix.two-dimensional-prefix-and-difference
type: cloze
anki: 1789002113270
tags: [concept-cloze, leetcode, recall, template]
---
二维矩形和通过 {{c1::四项容斥}} 从二维前缀表取得。

```
def range_add(n, updates):
    diff = [0] * (n + 1)
    for left, right, val in updates:
        diff[left] += val
        if right + 1 < len(diff):
            diff[right + 1] -= val
    for i in range(1, n):
        diff[i] += diff[i - 1]
    return diff[:n]
```

**Evidence**

§1.6 二维前缀和

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.04%20-%20%E4%BA%8C%E7%BB%B4%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E4%BA%8C%E7%BB%B4%E5%B7%AE%E5%88%86)
