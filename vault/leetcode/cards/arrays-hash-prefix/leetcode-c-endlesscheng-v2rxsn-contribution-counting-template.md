---
id: leetcode-c-endlesscheng-v2rxsn-contribution-counting-template
node: arrays-hash-prefix.contribution-counting
type: cloze
anki: 1787272464380
tags: [concept-cloze, leetcode, recall, template]
---
nums[i] 出现在连续子数组中的次数是 {{c1::(i + 1) * (n - i)}}。

```
def sum_subarray_sums(nums):
    n = len(nums)
    total = 0
    for i, value in enumerate(nums):
        total += value * (i + 1) * (n - i)
    return total
```

**Evidence**

一、技巧类题目：贡献法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.06%20-%20%E8%B4%A1%E7%8C%AE%E6%B3%95)
