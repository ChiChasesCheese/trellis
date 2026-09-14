---
id: leetcode-c-endlesscheng-0vinmk-fixed-length-sliding-window-template
node: two-pointers-window.fixed-length-sliding-window
type: cloze
anki: 1787268626341
tags: [concept-cloze, leetcode, recall, template]
---
定长滑动窗口模板中,右指针入队元素后,若right < k - 1 需要 {{c1::continue}} 跳过结算,窗口满后再让 left 出队。

```
def solve(nums, k):
    ans = 0
    window_sum = 0
    for right, x in enumerate(nums):
        # 1. enter window
        window_sum += x
        if right < k - 1:
            continue
        # 2. update answer
        ans = max(ans, window_sum)
        # 3. leave window
        left = right - k + 1
        window_sum -= nums[left]
    return ans
```

**Evidence**

§1.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.01%20-%20%E5%AE%9A%E9%95%BF%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
