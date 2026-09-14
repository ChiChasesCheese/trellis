---
id: leetcode-c-endlesscheng-mor1u6-offline-query-ordering-template
node: advanced-ds-heap.offline-query-ordering
type: cloze
anki: 1789002116720
tags: [concept-cloze, leetcode, recall, template]
---
离线查询排序前应保存 {{c1::enumerate(queries)}} 中的原始编号。

```
def offline_queries(queries):
    ordered = sorted(enumerate(queries), key=lambda item: item[1])
    ans = [None] * len(queries)
    state = 0
    for index, query in ordered:
        state += query
        ans[index] = state
    return ans
```

**Evidence**

专题：离线算法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.20%20-%20%E7%A6%BB%E7%BA%BF%E7%AE%97%E6%B3%95)
