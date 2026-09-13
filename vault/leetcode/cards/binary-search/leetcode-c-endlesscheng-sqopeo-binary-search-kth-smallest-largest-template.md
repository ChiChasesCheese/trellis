---
id: leetcode-c-endlesscheng-sqopeo-binary-search-kth-smallest-largest-template
node: binary-search.binary-search-kth-smallest-largest
type: cloze
anki: 1787272402506
tags: [concept-cloze, leetcode, recall, template]
---
kth_smallest 模板中内部的 check(x) 定义为 {{c1::count_le(x) >= k}}，随后复用二分答案求{{c2::最小}}的模板求解。

```
def kth_smallest(count_le, left, right, k):
    # count_le(x): number of elements <= x; monotonic non-decreasing in x
    def check(x):
        return count_le(x) >= k
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid
        else:
            left = mid
    return right
```

**Evidence**

§2.6 第 K 小/大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.08%20-%20%E7%AC%AC%20K%20%E5%B0%8F-%E5%A4%A7%E8%BD%AC%E5%8C%96%E4%B8%BA%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
