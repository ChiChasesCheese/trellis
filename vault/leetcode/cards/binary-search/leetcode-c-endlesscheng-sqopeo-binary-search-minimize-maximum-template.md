---
id: leetcode-c-endlesscheng-sqopeo-binary-search-minimize-maximum-template
node: binary-search.binary-search-minimize-maximum
type: cloze
anki: 1787272401904
tags: [concept-cloze, leetcode, recall, template]
---
minimize_max 模板与求最小模板一致：check(mid) 为真时更新 {{c1::right = mid}}，最终返回 {{c2::right}}。

```
def minimize_max(check, left, right):
    # check(cap): can we satisfy the constraints if the max is capped at `cap`?
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid
        else:
            left = mid
    return right
```

**Evidence**

§2.4 最小化最大值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.06%20-%20%E6%9C%80%E5%B0%8F%E5%8C%96%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%88%E4%BA%8C%E5%88%86%E4%B8%8A%E7%95%8C%EF%BC%89)
