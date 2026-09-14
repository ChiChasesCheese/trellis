---
id: leetcode-c-endlesscheng-wr1mjp-binary-search-on-answer-template
node: binary-search.binary-search-on-answer
type: cloze
anki: 1787272470380
tags: [concept-cloze, leetcode, recall, template]
---
二分答案需要的核心接口是 {{c1::feasible(candidate) -> bool}}，且结果对 candidate 单调。

```
def first_true(lo, hi, feasible):
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def minimize_limit(nums):
    def feasible(limit):
        carry = 0
        for x in nums:
            carry += x
            if carry > limit:
                return False
        return True
    return first_true(max(nums), sum(nums), feasible)
```

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.03%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
