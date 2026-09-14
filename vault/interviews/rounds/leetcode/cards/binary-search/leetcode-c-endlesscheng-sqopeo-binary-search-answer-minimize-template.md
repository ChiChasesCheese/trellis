---
id: leetcode-c-endlesscheng-sqopeo-binary-search-answer-minimize-template
node: binary-search.binary-search-answer-minimize
type: cloze
anki: 1787272401005
tags: [concept-cloze, leetcode, recall, template]
---
binary_search_min 模板中，当 check(mid) 为真时更新 {{c1::right = mid}}，循环结束返回 {{c2::right}}。

```
def binary_search_min(check, left, right):
    # invariant: check(left) is always False; check(right) is always True
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid
        else:
            left = mid
    return right
```

**Evidence**

§2.1 求最小 开区间二分模板

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.03%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88%E6%B1%82%E6%9C%80%E5%B0%8F%E5%80%BC%EF%BC%88%E5%BC%80%E5%8C%BA%E9%97%B4%E6%A8%A1%E6%9D%BF%EF%BC%89)
