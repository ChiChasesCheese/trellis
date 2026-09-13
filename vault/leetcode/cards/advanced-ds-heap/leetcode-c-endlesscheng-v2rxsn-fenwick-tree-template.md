---
id: leetcode-c-endlesscheng-v2rxsn-fenwick-tree-template
node: advanced-ds-heap.fenwick-tree
type: cloze
anki: 1787272467979
tags: [concept-cloze, leetcode, recall, template]
---
Fenwick 单点更新沿 {{c1::i += i & -i}} 向上修改。

```
class Fenwick:
    def __init__(self, n):
        self.tree = [0] * (n + 1)
    def add(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i
    def prefix_sum(self, i):
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total
```

**Evidence**

四、数据结构：树状数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.18%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%20Fenwick%20Tree)
