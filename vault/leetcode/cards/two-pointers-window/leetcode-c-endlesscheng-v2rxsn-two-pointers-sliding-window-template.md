---
id: leetcode-c-endlesscheng-v2rxsn-two-pointers-sliding-window-template
node: two-pointers-window.two-pointers-sliding-window
type: cloze
anki: 1787272462880
tags: [concept-cloze, leetcode, recall, template]
---
滑动窗口中 right 每次右移后，应先更新状态，再用 {{c1::while}} 循环移动 left 直到合法。

```
def longest_at_most_k(nums, k):
    left = 0
    total = 0
    best = 0
    for right, value in enumerate(nums):
        total += value
        while total > k:
            total -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best
```

**Evidence**

一、技巧类题目：双指针、滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.01%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E4%B8%8E%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
