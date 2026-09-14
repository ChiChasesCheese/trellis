---
id: leetcode-c-endlesscheng-sqopeo-binary-search-lower-bound-template
node: binary-search.binary-search-lower-bound
type: cloze
anki: 1787272400405
tags: [concept-cloze, leetcode, recall, template]
---
lower_bound 模板中循环条件是 {{c1::left < right}}，当 nums[mid] >= target 时更新 {{c2::right = mid}}。

```
def lower_bound(nums, target):
    # Return first index i such that nums[i] >= target; len(nums) if none
    left, right = 0, len(nums)  # closed-open interval [left, right)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] >= target:
            right = mid
        else:
            left = mid + 1
    return left
```

**Evidence**

一、二分查找 lowerBound 模板

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.01%20-%20%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE%E4%B8%8E%20lowerBound%20%E7%BB%9F%E4%B8%80%E8%BD%AC%E5%8C%96)
