---
id: leetcode-c-endlesscheng-sqopeo-binary-search-answer-maximize-template
node: binary-search.binary-search-answer-maximize
type: cloze
anki: 1787272401305
tags: [concept-cloze, leetcode, recall, template]
---
binary_search_max 模板中 check(mid) 为真时更新 {{c1::left = mid}}，循环结束返回 {{c2::left}}。

```
def binary_search_max(check, left, right):
    # invariant: check(left) is always True; check(right) is always False
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            left = mid
        else:
            right = mid
    return left
```

**Evidence**

§2.2 求最大 开区间二分模板

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.04%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88%E6%B1%82%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%88%E5%BC%80%E5%8C%BA%E9%97%B4%E6%A8%A1%E6%9D%BF%EF%BC%89)
