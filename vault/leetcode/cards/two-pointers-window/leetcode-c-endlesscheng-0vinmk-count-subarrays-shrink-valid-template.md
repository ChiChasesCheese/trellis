---
id: leetcode-c-endlesscheng-0vinmk-count-subarrays-shrink-valid-template
node: two-pointers-window.count-subarrays-shrink-valid
type: cloze
anki: 1787268627236
tags: [concept-cloze, leetcode, recall, template]
---
越短越合法计数模板中,内层while收缩到窗口合法后,累加语句是 ans += {{c1::right - left + 1}}。

```
def count_subarrays(nums, k):
    ans = 0
    left = 0
    window_sum = 0
    for right, x in enumerate(nums):
        window_sum += x
        while window_sum > k:  # shrink until valid
            window_sum -= nums[left]
            left += 1
        ans += right - left + 1  # all subarrays ending at right with start in [left, right]
    return ans
```

**Evidence**

§2.3.1 越短越合法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.04%20-%20%E5%AE%9A%E9%95%BF%E6%94%B6%E7%BC%A9%E8%AE%A1%E6%95%B0%E6%B3%95%EF%BC%88%E8%B6%8A%E7%9F%AD%E8%B6%8A%E5%90%88%E6%B3%95%EF%BC%89)
