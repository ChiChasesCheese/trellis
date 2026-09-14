---
id: leetcode-c-endlesscheng-mor1u6-enumerate-middle-and-diagonals-template
node: arrays-hash-prefix.enumerate-middle-and-diagonals
type: cloze
anki: 1789002112595
tags: [concept-cloze, leetcode, recall, template]
---
固定中间 j 后，左侧范围是 {{c1::[0,j)}}，右侧范围是 {{c2::(j,n)}}。

```
def diagonal_groups(grid):
    groups = {}
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            groups.setdefault(r - c, []).append(x)
    return groups
```

**Evidence**

§0.2 枚举中间

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.02%20-%20%E6%9E%9A%E4%B8%BE%E4%B8%AD%E9%97%B4%E4%B8%8E%E5%AF%B9%E8%A7%92%E7%BA%BF%E5%88%86%E7%BB%84)
