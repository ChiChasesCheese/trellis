---
id: leetcode-c-endlesscheng-sjfwqi-suffix-array-template
node: strings.suffix-array
type: cloze
anki: 1787272449381
tags: [concept-cloze, leetcode, recall, template]
---
后缀数组倍增法每轮按 {{c1::(rank[i], rank[i + step])}} 排序后缀。

```
def suffix_array(s):
    n = len(s)
    sa = list(range(n))
    rank = [ord(ch) for ch in s]
    step = 1
    while step < n:
        sa.sort(key=lambda i: (rank[i], rank[i + step] if i + step < n else -1))
        new_rank = [0] * n
        for pos in range(1, n):
            a, b = sa[pos - 1], sa[pos]
            if (rank[a], rank[a + step] if a + step < n else -1) != (rank[b], rank[b + step] if b + step < n else -1):
                new_rank[b] = new_rank[a] + 1
            else:
                new_rank[b] = new_rank[a]
        rank = new_rank
        step *= 2
    return sa
```

**Evidence**

八、后缀数组/后缀自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.08%20-%20%E5%90%8E%E7%BC%80%E6%95%B0%E7%BB%84%20%28Suffix%20Array%29)
