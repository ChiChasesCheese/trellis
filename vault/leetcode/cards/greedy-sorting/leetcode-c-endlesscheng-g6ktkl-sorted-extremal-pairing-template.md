---
id: leetcode-c-endlesscheng-g6ktkl-sorted-extremal-pairing-template
node: greedy-sorting.sorted-extremal-pairing
type: cloze
anki: 1787272431605
tags: [concept-cloze, leetcode, recall, template]
---
双序列配对模板中，当前 a[i] 无法匹配 b[j] 时，应移动 {{c1::b 的指针}} 来寻找更大的候选。

```
def max_pairs(a: list[int], b: list[int]) -> int:
    a.sort()
    b.sort()
    i = j = pairs = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            pairs += 1
            i += 1
            j += 1
        else:
            j += 1
    return pairs
```

**Evidence**

§1.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.01%20-%20%E6%8E%92%E5%BA%8F%E5%90%8E%E7%9A%84%E6%9E%81%E5%80%BC%E4%B8%8E%E9%85%8D%E5%AF%B9%E8%B4%AA%E5%BF%83)
