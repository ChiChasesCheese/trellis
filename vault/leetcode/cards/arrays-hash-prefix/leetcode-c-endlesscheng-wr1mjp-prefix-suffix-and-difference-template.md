---
id: leetcode-c-endlesscheng-wr1mjp-prefix-suffix-and-difference-template
node: arrays-hash-prefix.prefix-suffix-and-difference
type: cloze
anki: 1787272470680
tags: [concept-cloze, leetcode, recall, template]
---
闭区间 [l, r] 加 delta 的差分更新为 {{c1::d[l] += delta；d[r + 1] -= delta（若存在）}}。

```
def range_add(n, updates):
    diff = [0] * (n + 1)
    for left, right, delta in updates:
        diff[left] += delta
        if right + 1 < n:
            diff[right + 1] -= delta
    ans = [0] * n
    running = 0
    for i in range(n):
        running += diff[i]
        ans[i] = running
    return ans
```

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.04%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E3%80%81%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%B7%AE%E5%88%86)
