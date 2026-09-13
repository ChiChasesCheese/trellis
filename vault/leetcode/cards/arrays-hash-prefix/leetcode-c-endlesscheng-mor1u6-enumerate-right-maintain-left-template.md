---
id: leetcode-c-endlesscheng-mor1u6-enumerate-right-maintain-left-template
node: arrays-hash-prefix.enumerate-right-maintain-left
type: cloze
anki: 1787272418106
tags: [concept-cloze, leetcode, recall, template]
---
有顺序的两数匹配中，应先 {{c1::查询 need}}，再 {{c2::写入当前值}}。

```
def two_sum_ordered(nums, target):
    seen = {}
    for j, x in enumerate(nums):
        need = target - x
        if need in seen:
            return seen[need], j
        seen[x] = j
    return None
```

**Evidence**

§0.1 枚举右，维护左

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.01%20-%20%E6%9E%9A%E4%B8%BE%E5%8F%B3%E7%AB%AF%E3%80%81%E7%BB%B4%E6%8A%A4%E5%B7%A6%E7%AB%AF)
