---
id: leetcode-c-endlesscheng-v2rxsn-kadane-maximum-subarray-template
node: arrays-hash-prefix.kadane-maximum-subarray
type: cloze
anki: 1787272464980
tags: [concept-cloze, leetcode, recall, template]
---
Kadane 转移为 end_here = max(value, {{c1::end_here + value}})。

```
def max_subarray(nums):
    end_here = nums[0]
    best = nums[0]
    for value in nums[1:]:
        end_here = max(value, end_here + value)
        best = max(best, end_here)
    return best
```

**Evidence**

二、动态规划：最大子数组和

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.08%20-%20%E6%9C%80%E5%A4%A7%E5%AD%90%E6%95%B0%E7%BB%84%E5%92%8C%20Kadane)
