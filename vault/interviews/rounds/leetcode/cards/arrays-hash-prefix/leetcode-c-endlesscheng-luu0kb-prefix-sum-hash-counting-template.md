---
id: leetcode-c-endlesscheng-luu0kb-prefix-sum-hash-counting-template
node: arrays-hash-prefix.prefix-sum-hash-counting
type: cloze
anki: 1787272457179
tags: [concept-cloze, leetcode, recall, template]
---
统计和为 k 的子数组时，当前位置贡献为 count[{{c1::prefix - k}}]。

```
from collections import defaultdict

def count_subarrays_sum_k(nums, k):
    count = defaultdict(int)
    count[0] = 1
    prefix = 0
    answer = 0
    for value in nums:
        prefix += value
        answer += count[prefix - k]
        count[prefix] += 1
    return answer
```

**Evidence**

一、技巧类题目：前缀和、哈希表

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.05%20-%20%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%93%88%E5%B8%8C%E8%AE%A1%E6%95%B0)
