---
id: leetcode-c-endlesscheng-v2rxsn-prefix-sum-difference-array-template
node: arrays-hash-prefix.prefix-sum-difference-array
type: cloze
anki: 1787272463479
tags: [concept-cloze, leetcode, recall, template]
---
差分数组恢复原数组时，从左到右做一次 {{c1::累计和}}。

```
def range_add(n, updates):
    diff = [0] * (n + 1)
    for left, right, value in updates:
        diff[left] += value
        diff[right + 1] -= value
    ans = []
    current = 0
    for i in range(n):
        current += diff[i]
        ans.append(current)
    return ans
```

**Evidence**

一、技巧类题目：前缀和、差分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.03%20-%20%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%B7%AE%E5%88%86)
