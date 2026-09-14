---
id: leetcode-c-endlesscheng-g6ktkl-component-swapping-template
node: graphs-traversal.component-swapping
type: cloze
anki: 1787272438206
tags: [concept-cloze, leetcode, recall, template]
---
并查集分组后，字典序最小回填要把 {{c1::排序后的字符}} 放回排序后的索引。

```
def smallest_by_swaps(s: str, pairs: list[list[int]]) -> str:
    parent = list(range(len(s)))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    groups: dict[int, list[int]] = {}
    for i in range(len(s)):
        groups.setdefault(find(i), []).append(i)
    result = list(s)
    for indices in groups.values():
        chars = sorted(result[i] for i in indices)
        for i, ch in zip(sorted(indices), chars):
            result[i] = ch
    return ''.join(result)
```

**Evidence**

§5.7

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.23%20-%20%E8%BF%9E%E9%80%9A%E5%9D%97%E5%86%85%E4%BA%A4%E6%8D%A2)
