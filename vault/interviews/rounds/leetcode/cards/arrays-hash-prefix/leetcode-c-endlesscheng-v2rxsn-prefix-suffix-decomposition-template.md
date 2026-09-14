---
id: leetcode-c-endlesscheng-v2rxsn-prefix-suffix-decomposition-template
node: arrays-hash-prefix.prefix-suffix-decomposition
type: cloze
anki: 1787272464079
tags: [concept-cloze, leetcode, recall, template]
---
前缀和常定义为 left[i] 表示 {{c1::前 i 个元素}} 的和。

```
def best_split(nums):
    n = len(nums)
    left = [0] * (n + 1)
    for i in range(n):
        left[i + 1] = left[i] + nums[i]
    right = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        right[i] = right[i + 1] + nums[i]
    return max(left[i] - right[i] for i in range(n + 1))
```

**Evidence**

一、技巧类题目：前后缀分解

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.05%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%88%86%E8%A7%A3)
