---
id: leetcode-c-endlesscheng-wr1mjp-two-pointers-and-sliding-window-template
node: two-pointers-window.two-pointers-and-sliding-window
type: cloze
anki: 1787272470082
tags: [concept-cloze, leetcode, recall, template]
---
窗口模板的顺序是 {{c1::加入 nums[right]，while 不合法则移除 nums[left] 并 left += 1，再更新答案}}。

```
from collections import defaultdict

def longest_valid(nums, limit):
    count = defaultdict(int)
    left = 0
    best = 0
    for right, x in enumerate(nums):
        count[x] += 1
        while len(count) > limit:
            y = nums[left]
            count[y] -= 1
            if count[y] == 0:
                del count[y]
            left += 1
        best = max(best, right - left + 1)
    return best
```

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.02%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E4%B8%8E%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
