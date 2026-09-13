---
id: leetcode-c-endlesscheng-0vinmk-same-direction-two-pointers-template
node: two-pointers-window.same-direction-two-pointers
type: cloze
anki: 1787268628437
tags: [concept-cloze, leetcode, recall, template]
---
同向双指针模板中,内层while移动的是left指针,并且规定它{{c1::永不回退(only left += 1)}}。

```
def solve(nums):
    left = 0
    for right, x in enumerate(nums):
        # move right pointer forward (enter window)
        while some_condition(nums, left, right):
            # move left pointer forward, never backward
            left += 1
    return left
```

**Evidence**

§3.3 同向双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.08%20-%20%E5%90%8C%E5%90%91%E5%8F%8C%E6%8C%87%E9%92%88)
