---
id: leetcode-c-endlesscheng-g6ktkl-product-and-inequality-greedy-template
node: greedy-sorting.product-and-inequality-greedy
type: cloze
anki: 1787272435507
tags: [concept-cloze, leetcode, recall, template]
---
把 total 分成 parts 份时，用 {{c1::divmod(total, parts)}} 获得基础值和需加一的份数。

```
def max_product_partition(total: int, parts: int) -> int:
    small, extra = divmod(total, parts)
    product = 1
    for i in range(parts):
        product *= small + (i < extra)
    return product
```

**Evidence**

§4.4

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.14%20-%20%E4%B9%98%E7%A7%AF%E8%B4%AA%E5%BF%83%E4%B8%8E%E4%B8%8D%E7%AD%89%E5%BC%8F)
