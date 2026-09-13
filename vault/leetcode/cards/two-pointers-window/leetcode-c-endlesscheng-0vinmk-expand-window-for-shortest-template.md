---
id: leetcode-c-endlesscheng-0vinmk-expand-window-for-shortest-template
node: two-pointers-window.expand-window-for-shortest
type: cloze
anki: 1787268626937
tags: [concept-cloze, leetcode, recall, template]
---
扩张式滑窗模板中,内层收缩循环的条件是{{c1::window_sum >= target}},即窗口合法时才尝试收缩left。

```
def solve(nums, target):
    ans = float('inf')
    left = 0
    window_sum = 0
    for right, x in enumerate(nums):
        window_sum += x  # enter window
        while window_sum >= target:  # window valid, try to shrink
            ans = min(ans, right - left + 1)
            window_sum -= nums[left]
            left += 1
    return ans if ans != float('inf') else 0
```

**Evidence**

§2.2 越长越合法/求最短/最小

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.03%20-%20%E6%89%A9%E5%BC%A0%E5%BC%8F%E4%B8%8D%E5%AE%9A%E9%95%BF%E6%BB%91%E7%AA%97%EF%BC%88%E6%B1%82%E6%9C%80%E7%9F%AD-%E6%9C%80%E5%B0%8F%EF%BC%89)
