---
id: leetcode-c-endlesscheng-iyt3ss-probability-expectation-dp-template
node: dp-game-probability.probability-expectation-dp
type: cloze
anki: 1787272428004
tags: [concept-cloze, leetcode, recall, template]
---
状态有自环概率 stay 时，E 的分母需要是 {{c1::1-stay}}。

```
def expected_steps(probabilities):
    expected = [0.0] * (len(probabilities) + 1)
    for state in range(len(probabilities) - 1, -1, -1):
        stay = probabilities[state][0]
        move = probabilities[state][1:]
        if stay >= 1.0:
            return float('inf')
        expected[state] = (1.0 + sum(p * expected[state + i] for i, p in enumerate(move, 1))) / (1.0 - stay)
    return expected[0]
```

**Evidence**

三、概率期望

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.11%20-%20%E6%A6%82%E7%8E%87%E6%9C%9F%E6%9C%9B%E4%B8%8E%E6%9C%9F%E6%9C%9B%20DP)
