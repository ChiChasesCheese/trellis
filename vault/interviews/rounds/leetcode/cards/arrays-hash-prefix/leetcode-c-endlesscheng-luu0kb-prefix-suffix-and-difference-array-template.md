---
id: leetcode-c-endlesscheng-luu0kb-prefix-suffix-and-difference-array-template
node: arrays-hash-prefix.prefix-suffix-and-difference-array
type: cloze
anki: 1787272456880
tags: [concept-cloze, leetcode, recall, template]
---
差分数组必须对 diff 再做一次 {{c1::前缀和}} 才能得到实际数组。

```
def range_add(n, updates):
    diff = [0] * (n + 1)
    for left, right, delta in updates:
        diff[left] += delta
        if right + 1 < n:
            diff[right + 1] -= delta
    nums = [0] * n
    running = 0
    for i in range(n):
        running += diff[i]
        nums[i] = running
    return nums
```

**Evidence**

一、技巧类题目：差分数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.04%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%88%86%E8%A7%A3%E4%B8%8E%E5%B7%AE%E5%88%86%E6%95%B0%E7%BB%84)
