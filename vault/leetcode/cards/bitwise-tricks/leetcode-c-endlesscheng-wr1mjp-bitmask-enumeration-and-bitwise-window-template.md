---
id: leetcode-c-endlesscheng-wr1mjp-bitmask-enumeration-and-bitwise-window-template
node: bitwise-tricks.bitmask-enumeration-and-bitwise-window
type: cloze
anki: 1787272470981
tags: [concept-cloze, leetcode, recall, template]
---
位冲突窗口的收缩条件是 {{c1::while mask & x}}。

```
def max_disjoint_bitwise(nums):
    left = 0
    mask = 0
    best = 0
    for right, x in enumerate(nums):
        while mask & x:
            mask ^= nums[left]
            left += 1
        mask |= x
        best = max(best, right - left + 1)
    return best
```

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.05%20-%20%E4%BD%8D%E8%BF%90%E7%AE%97%E4%B8%8E%E4%BA%8C%E8%BF%9B%E5%88%B6%E6%9E%9A%E4%B8%BE)
