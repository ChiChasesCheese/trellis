---
id: leetcode-c-endlesscheng-sqopeo-binary-search-sort-then-search-template
node: binary-search.binary-search-sort-then-search
type: cloze
anki: 1787272400705
tags: [concept-cloze, leetcode, recall, template]
---
先排序再二分的整体复杂度为排序的 {{c1::O(n log n)}} 加上每次查询的 {{c2::O(log n)}}。

```
def solve_after_sort(nums, x):
    nums.sort()  # establish monotonicity
    return lower_bound(nums, x)  # reuse lower_bound template
```

**Evidence**

§1.2 进阶

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.02%20-%20%E5%85%88%E6%8E%92%E5%BA%8F%E5%86%8D%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE)
