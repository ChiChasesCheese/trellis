---
id: leetcode-c-endlesscheng-mor1u6-fenwick-tree-and-inversion-count-template
node: advanced-ds-heap.fenwick-tree-and-inversion-count
type: cloze
anki: 1789002115320
tags: [concept-cloze, leetcode, recall, template]
---
闭区间 [l,r] 的和写作 {{c1::prefix(r)-prefix(l-1)}}。

```
class Fenwick:
    def __init__(self, n):
        self.t = [0] * (n + 1)

    def add(self, i, delta):
        while i < len(self.t):
            self.t[i] += delta
            i += i & -i

    def prefix(self, i):
        total = 0
        while i:
            total += self.t[i]
            i -= i & -i
        return total
```

**Evidence**

§8.1 树状数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.14%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E3%80%81%E5%80%BC%E5%9F%9F%E7%BB%9F%E8%AE%A1%E4%B8%8E%E9%80%86%E5%BA%8F%E5%AF%B9)
