---
id: leetcode-c-endlesscheng-txls3i-dag-game-probability-expectation-dp-template
node: dp-game-probability.dag-game-probability-expectation-dp
type: cloze
anki: 1787272417507
tags: [concept-cloze, leetcode, recall, template]
---
期望 DP 的基本形式是 {{c1::概率乘后继值的加权和}}。

```
def solve(values):
    dp = [0] * (len(values) + 1)
    for i in range(len(values) - 1, -1, -1):
        dp[i] = max(values[i] - dp[i + 1], 0)
    return dp[0]
```

**Evidence**

十五、概率 DP、期望 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.20%20-%20%E5%9B%BE%E3%80%81%E5%8D%9A%E5%BC%88%E4%B8%8E%E6%A6%82%E7%8E%87%E6%9C%9F%E6%9C%9B%20DP)
