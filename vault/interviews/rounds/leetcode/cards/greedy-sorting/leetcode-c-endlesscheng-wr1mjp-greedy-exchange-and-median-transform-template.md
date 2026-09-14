---
id: leetcode-c-endlesscheng-wr1mjp-greedy-exchange-and-median-transform-template
node: greedy-sorting.greedy-exchange-and-median-transform
type: cloze
anki: 1787272475781
tags: [concept-cloze, leetcode, recall, template]
---
加权绝对距离和最小化时，应在排序后找累计权重首次达到总权重一半的 {{c1::加权中位数}}。

```
def min_cost_to_equal(nums, cost):
    pairs = sorted(zip(nums, cost))
    total = sum(cost)
    prefix = 0
    target = pairs[0][0]
    for value, weight in pairs:
        prefix += weight
        if prefix * 2 >= total:
            target = value
            break
    return sum(abs(value - target) * weight for value, weight in pairs)
```

**Evidence**

7. 思维题

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.21%20-%20%E8%B4%AA%E5%BF%83%E3%80%81%E7%AD%89%E4%BB%B7%E8%BD%AC%E6%8D%A2%E4%B8%8E%E4%B8%AD%E4%BD%8D%E6%95%B0)
