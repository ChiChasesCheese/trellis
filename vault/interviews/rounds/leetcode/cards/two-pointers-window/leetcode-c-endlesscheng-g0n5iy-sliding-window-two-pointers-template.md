---
id: leetcode-c-endlesscheng-g0n5iy-sliding-window-two-pointers-template
node: two-pointers-window.sliding-window-two-pointers
type: cloze
anki: 1787272476380
tags: [concept-cloze, leetcode, recall, template]
---
满足条件的窗口计数常在右端固定后增加 {{c1::right - left + 1}}。

```
def count_valid(nums, limit):
    left = 0
    total = 0
    value = 0
    for right, x in enumerate(nums):
        value += x
        while left <= right and value >= limit:
            value -= nums[left]
            left += 1
        total += right - left + 1
    return total
```

**Evidence**

双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.02%20-%20%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E5%8F%8C%E6%8C%87%E9%92%88)
