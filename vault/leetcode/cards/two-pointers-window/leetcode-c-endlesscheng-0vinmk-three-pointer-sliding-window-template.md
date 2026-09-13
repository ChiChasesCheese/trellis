---
id: leetcode-c-endlesscheng-0vinmk-three-pointer-sliding-window-template
node: two-pointers-window.three-pointer-sliding-window
type: cloze
anki: 1787268629037
tags: [concept-cloze, leetcode, recall, template]
---
三指针滑动窗口模板中,每次right右移后,最终答案的累加语句是 ans += {{c1::left1 - left2}}。

```
def count_exactly_k(nums, k):
    ans = 0
    left1 = left2 = 0
    sum1 = sum2 = 0
    for right, x in enumerate(nums):
        sum1 += x
        sum2 += x
        while left1 <= right and sum1 >= k:  # threshold k
            sum1 -= nums[left1]
            left1 += 1
        while left2 <= right and sum2 >= k + 1:  # threshold k + 1
            sum2 -= nums[left2]
            left2 += 1
        ans += left1 - left2  # count with sum exactly k ending at right
    return ans
```

**Evidence**

§2.3.3 恰好型滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.10%20-%20%E4%B8%89%E6%8C%87%E9%92%88%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
