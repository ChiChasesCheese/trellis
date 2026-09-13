---
id: leetcode-c-endlesscheng-0vinmk-shrink-window-for-longest-template
node: two-pointers-window.shrink-window-for-longest
type: cloze
anki: 1787268626636
tags: [concept-cloze, leetcode, recall, template]
---
收缩式滑窗模板中,内层收缩循环的条件是{{c1::window_state > k}},即窗口不合法时才收缩left。

```
def solve(nums, k):
    ans = 0
    left = 0
    window_state = 0
    for right, x in enumerate(nums):
        window_state += x  # enter window
        while window_state > k:  # window invalid, shrink
            window_state -= nums[left]
            left += 1
        ans = max(ans, right - left + 1)
    return ans
```

**Evidence**

§2.1 越短越合法/求最长/最大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.02%20-%20%E6%94%B6%E7%BC%A9%E5%BC%8F%E4%B8%8D%E5%AE%9A%E9%95%BF%E6%BB%91%E7%AA%97%EF%BC%88%E6%B1%82%E6%9C%80%E9%95%BF-%E6%9C%80%E5%A4%A7%EF%BC%89)
