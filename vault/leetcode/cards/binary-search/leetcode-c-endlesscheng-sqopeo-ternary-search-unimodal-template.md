---
id: leetcode-c-endlesscheng-sqopeo-ternary-search-unimodal-template
node: binary-search.ternary-search-unimodal
type: cloze
anki: 1787272402805
tags: [concept-cloze, leetcode, recall, template]
---
ternary_search_max 模板每轮取两个三等分点 m1、m2，若 f(m1) < f(m2) 则更新 {{c1::left = m1}}，否则更新 {{c2::right = m2}}。

```
def ternary_search_max(f, left, right, eps=1e-9):
    # f is unimodal (increases then decreases) on [left, right]
    while right - left > eps:
        m1 = left + (right - left) / 3
        m2 = right - (right - left) / 3
        if f(m1) < f(m2):
            left = m1
        else:
            right = m2
    return (left + right) / 2
```

**Evidence**

三、三分法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.09%20-%20%E4%B8%89%E5%88%86%E6%B3%95%E6%B1%82%E5%8D%95%E5%B3%B0%E5%87%BD%E6%95%B0%E6%9E%81%E5%80%BC)
