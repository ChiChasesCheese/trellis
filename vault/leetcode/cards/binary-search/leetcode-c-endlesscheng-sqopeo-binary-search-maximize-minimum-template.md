---
id: leetcode-c-endlesscheng-sqopeo-binary-search-maximize-minimum-template
node: binary-search.binary-search-maximize-minimum
type: cloze
anki: 1787272402206
tags: [concept-cloze, leetcode, recall, template]
---
maximize_min 模板与求最大模板一致：check(mid) 为真时更新 {{c1::left = mid}}，最终返回 {{c2::left}}。

```
def maximize_min(check, left, right):
    # check(floor): can we satisfy the constraints if the min is at least `floor`?
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            left = mid
        else:
            right = mid
    return left
```

**Evidence**

§2.5 最大化最小值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.07%20-%20%E6%9C%80%E5%A4%A7%E5%8C%96%E6%9C%80%E5%B0%8F%E5%80%BC%EF%BC%88%E4%BA%8C%E5%88%86%E4%B8%8B%E7%95%8C%EF%BC%89)
