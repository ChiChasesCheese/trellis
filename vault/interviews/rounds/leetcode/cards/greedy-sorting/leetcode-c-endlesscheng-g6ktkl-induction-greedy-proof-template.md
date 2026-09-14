---
id: leetcode-c-endlesscheng-g6ktkl-induction-greedy-proof-template
node: greedy-sorting.induction-greedy-proof
type: cloze
anki: 1787272436407
tags: [concept-cloze, leetcode, recall, template]
---
递归归纳骨架是先处理一个安全首步，再对 {{c1::更小的同类实例}} 调用自身。

```
def choose_minimum(nums: list[int]) -> list[int]:
    if not nums:
        return []
    first = min(nums)
    remaining = nums[:]
    remaining.remove(first)
    return [first] + choose_minimum(remaining)
```

**Evidence**

§4.6

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.17%20-%20%E5%BD%92%E7%BA%B3%E6%B3%95%E9%AA%8C%E8%AF%81%E8%B4%AA%E5%BF%83)
