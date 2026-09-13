---
id: leetcode-c-endlesscheng-iyt3ss-generating-functions-template
node: math-number-theory.generating-functions
type: cloze
anki: 1787272427707
tags: [concept-cloze, leetcode, recall, template]
---
完全背包计数中，coin 固定后 total 应从 {{c1::coin 向上}} 遍历。

```
def count_unbounded(coins, target, mod):
    ways = [0] * (target + 1)
    ways[0] = 1
    for coin in coins:
        for total in range(coin, target + 1):
            ways[total] = (ways[total] + ways[total - coin]) % mod
    return ways[target]
```

**Evidence**

§2.5 生成函数（母函数）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.10%20-%20%E7%94%9F%E6%88%90%E5%87%BD%E6%95%B0)
