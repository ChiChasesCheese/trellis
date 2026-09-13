---
id: leetcode-c-endlesscheng-sqopeo-binary-search-indirect-target-template
node: binary-search.binary-search-indirect-target
type: cloze
anki: 1787272401603
tags: [concept-cloze, leetcode, recall, template]
---
binary_search_indirect 模板在二分结束后，需要通过 {{c1::decode}} 函数把代理值{{c2::映射回真实答案}}，而不能直接返回代理值。

```
def binary_search_indirect(check, left, right, decode):
    # check operates on a proxy value that is monotonic w.r.t. feasibility
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid
        else:
            left = mid
    return decode(right)  # map proxy value back to the real answer
```

**Evidence**

§2.3 二分间接值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.05%20-%20%E4%BA%8C%E5%88%86%E9%97%B4%E6%8E%A5%E5%80%BC%E8%80%8C%E9%9D%9E%E7%9B%B4%E6%8E%A5%E7%AD%94%E6%A1%88)
