---
id: leetcode-c-endlesscheng-0vinmk-count-subarrays-expand-valid-template
node: two-pointers-window.count-subarrays-expand-valid
type: cloze
anki: 1787268627537
tags: [concept-cloze, leetcode, recall, template]
---
越长越合法计数模板中,内层while收缩到窗口不合法后,累加语句是 ans += {{c1::left}}。

```
def count_subarrays(nums, k):
    ans = 0
    left = 0
    window_sum = 0
    for right, x in enumerate(nums):
        window_sum += x
        while left <= right and window_sum >= k:  # shrink until invalid
            window_sum -= nums[left]
            left += 1
        ans += left  # subarrays with start in [0, left-1] ending at right are all valid
    return ans
```

**Evidence**

§2.3.2 越长越合法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.05%20-%20%E5%AE%9A%E9%95%BF%E6%89%A9%E5%BC%A0%E8%AE%A1%E6%95%B0%E6%B3%95%EF%BC%88%E8%B6%8A%E9%95%BF%E8%B6%8A%E5%90%88%E6%B3%95%EF%BC%89)
