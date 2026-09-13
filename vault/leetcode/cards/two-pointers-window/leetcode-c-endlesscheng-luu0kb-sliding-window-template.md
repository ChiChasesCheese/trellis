---
id: leetcode-c-endlesscheng-luu0kb-sliding-window-template
node: two-pointers-window.sliding-window
type: cloze
anki: 1787272455980
tags: [concept-cloze, leetcode, recall, template]
---
滑动窗口中每个元素最多被左右指针各跨过一次，因此通常是 {{c1::O(n)}}。

```
from collections import defaultdict

def longest_at_most_k(nums, k):
    count = defaultdict(int)
    left = 0
    best = 0
    for right, value in enumerate(nums):
        count[value] += 1
        while count[value] > k:
            count[nums[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

**Evidence**

一、技巧类题目：滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.01%20-%20%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
