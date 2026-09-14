---
id: leetcode-c-endlesscheng-mor1u6-sqrt-decomposition-and-mo-template
node: advanced-ds-heap.sqrt-decomposition-and-mo
type: cloze
anki: 1789002116295
tags: [concept-cloze, leetcode, recall, template]
---
基础分块中第 i 个元素所属块编号是 {{c1::i // block_size}}。

```
def block_sums(nums, block_size):
    blocks = [0] * ((len(nums) + block_size - 1) // block_size)
    for i, x in enumerate(nums):
        blocks[i // block_size] += x
    return blocks
```

**Evidence**

§10.1 分块

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.19%20-%20%E5%88%86%E5%9D%97%E3%80%81%E6%A0%B9%E5%8F%B7%E5%88%86%E8%A7%A3%E4%B8%8E%E8%8E%AB%E9%98%9F%E7%AE%97%E6%B3%95)
