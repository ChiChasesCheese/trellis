---
id: leetcode-c-endlesscheng-0vinmk-exactly-k-via-two-at-least-template
node: two-pointers-window.exactly-k-via-two-at-least
type: cloze
anki: 1787268627836
tags: [concept-cloze, leetcode, recall, template]
---
恰好型分解模板中,count_exactly_k(nums, k) 的实现是 solve_at_least(nums, k) - {{c1::solve_at_least(nums, k + 1)}}。

```
def solve_at_least(nums, k):
    # counts subarrays with sum >= k, via the expand-valid counting template
    ans = 0
    left = 0
    window_sum = 0
    for right, x in enumerate(nums):
        window_sum += x
        while left <= right and window_sum >= k:
            window_sum -= nums[left]
            left += 1
        ans += left
    return ans

def count_exactly_k(nums, k):
    return solve_at_least(nums, k) - solve_at_least(nums, k + 1)
```

**Evidence**

§2.3.3 恰好型滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.06%20-%20%E6%81%B0%E5%A5%BD%E5%9E%8B%E6%BB%91%E7%AA%97%E7%9A%84%E5%AE%B9%E6%96%A5%E5%88%86%E8%A7%A3)
