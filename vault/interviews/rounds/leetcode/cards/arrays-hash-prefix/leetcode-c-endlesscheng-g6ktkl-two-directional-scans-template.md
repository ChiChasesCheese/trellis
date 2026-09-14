---
id: leetcode-c-endlesscheng-g6ktkl-two-directional-scans-template
node: arrays-hash-prefix.two-directional-scans
type: cloze
anki: 1787272437905
tags: [concept-cloze, leetcode, recall, template]
---
右向扫描的典型循环是 {{c1::for i in range(n - 1, -1, -1)}}。

```
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer
```

**Evidence**

§5.6

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.22%20-%20%E4%B8%A4%E6%AC%A1%E6%89%AB%E6%8F%8F)
