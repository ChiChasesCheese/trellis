---
id: leetcode-c-endlesscheng-g6ktkl-contribution-counting-template
node: arrays-hash-prefix.contribution-counting
type: cloze
anki: 1787272437606
tags: [concept-cloze, leetcode, recall, template]
---
位置 i 的元素出现在连续子数组中的次数是 {{c1::(i + 1) * (n - i)}}。

```
def sum_of_all_subarray_sums(nums: list[int]) -> int:
    n = len(nums)
    total = 0
    for i, x in enumerate(nums):
        total += x * (i + 1) * (n - i)
    return total
```

**Evidence**

§5.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.21%20-%20%E8%B4%A1%E7%8C%AE%E6%B3%95)
