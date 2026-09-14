---
id: leetcode-c-endlesscheng-g6ktkl-enumerate-then-greedy-template
node: greedy-sorting.enumerate-then-greedy
type: cloze
anki: 1787272432207
tags: [concept-cloze, leetcode, recall, template]
---
枚举模板的外层循环负责 {{c1::固定关键状态}}，内层循环才执行贪心决策。

```
def best_value(nums: list[int]) -> int:
    answer = 0
    for first in range(len(nums)):
        total = nums[first]
        last = nums[first]
        for i, x in enumerate(nums):
            if i != first and x >= last:
                total += x
                last = x
        answer = max(answer, total)
    return answer
```

**Evidence**

§1.6

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.03%20-%20%E6%9E%9A%E4%B8%BE%E5%85%B3%E9%94%AE%E7%8A%B6%E6%80%81%E5%90%8E%E8%B4%AA%E5%BF%83)
